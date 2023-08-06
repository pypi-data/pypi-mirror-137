from etherscan.accounts import Account
from etherscan.client import EmptyResponse
import json
import datetime
from django.utils import timezone
#from ..portfolioConfig import BSC_EXPLORER_APIKEY
BSC_EXPLORER_APIKEY = "8NJAS8T7PCVQXKID9NW72AB6KX2XI8BKQE"


class AccountBsc(Account):
    PREFIX = "https://api.bscscan.com/api?"

class BscTransactions():
    def __init__(self,  bscAccountAddress, apiKey=BSC_EXPLORER_APIKEY):
        self.apiKey = apiKey
        self.address = bscAccountAddress.lower()
        self.bscScanAccountApi = AccountBsc(address=bscAccountAddress, api_key=self.apiKey)
        self.transactions = []
        self.erc20Transactions = []
        self.internalTranscations = []

    def update(self):
        try:
            self.transactions = self.bscScanAccountApi.get_transaction_page()
        except EmptyResponse:
            self.transactions = []
        try:
            self.erc20Transactions = self.bscScanAccountApi.get_transaction_page(erc20=True)
        except EmptyResponse:
            self.erc20Transactions = []
        try:
            self.internalTransactions = self.bscScanAccountApi.get_transaction_page(erc20=False, internal=True)
        except EmptyResponse:
            self.internalTransactions = []

    def getAllTransactions(self, startTime=None):
        self.update()
        normalTransactions = self.getTransactionsAsDict(erc20=False)
        erc20TransActions = self.getTransactionsAsDict(erc20=True)
        internalTransactions = self.getTransactionsAsDict(erc20=False, internal=True)
        allTransactions = normalTransactions + erc20TransActions + internalTransactions

        #print(allTransactions)

        # Check for swap:
        for normalTransaction in normalTransactions:
            for erc20TransAction in erc20TransActions:
                if normalTransaction["txId"] == erc20TransAction["txId"] and normalTransaction["time"] == erc20TransAction["time"]:
                    if erc20TransAction["category"] == "Trade":
                        raise("Unknown condition")
                    if erc20TransAction["category"] == "Transfer In":
                        erc20TransAction["category"] = "Swap"
                        erc20TransAction["fee"] = normalTransaction["fee"]
                        erc20TransAction["feeCurrency"] = normalTransaction["feeCurrency"]
                        erc20TransAction["amountOut"] = normalTransaction["amountOut"]
                        erc20TransAction["currencyOut"] = normalTransaction["currencyOut"]
                        allTransactions.remove(normalTransaction)
                    elif erc20TransAction["category"] == "Transfer Out":
                        print(erc20TransAction)
                        print("#####")
                        print(normalTransaction)
                        if "amountIn" in normalTransaction:
                        #if normalTransaction["txId"] == "0x7c1b0f2587e972cd54be7d840193b67f8bee6789b8cdba55607920d58f6ce5b1":
                        #    continue
                            erc20TransAction["category"] = "Swap"
                            erc20TransAction["amountIn"] = normalTransaction["amountIn"]
                            erc20TransAction["currencyOut"] = normalTransaction["currencyIn"]
                            allTransactions.remove(normalTransaction)
                        else:
                            # atomic swaps
                            # do not remove transaction, but add another one
                            erc20TransAction["category"] = "Swap"
                            t = erc20TransAction.copy()
                            t["category"] = "Swap"
                            t["amountIn"] = t["amountOut"]
                            t["currencyIn"] = t["currencyOut"]
                            t["fee"] = 0
                            t["amountOut"] = 0
                            t["note"] = "Atomic Swap"
                            allTransactions.append(t)

        # Remove elements that are before startTime
        # for transaction in allTransactions:

        return allTransactions

    def isTransactionInERC20Transactions(self, transaction):
        for erc20Transaction in self.erc20Transactions:
            if erc20Transaction["hash"] == transaction["hash"]:
                return True
        return False

    def getNumberOfInputAndOutputTokenTransactions(self, transaction):
        inputs = 0
        outputs = 0
        numTokens = 0
        tokenList = []
        for erc20Transaction in self.erc20Transactions:
            if erc20Transaction["hash"] == transaction["hash"]:
                if erc20Transaction["from"] == self.address and float(erc20Transaction["value"]) > 0:
                    outputs += 1
                if erc20Transaction["to"] == self.address and float(erc20Transaction["value"]) > 0:
                    inputs += 1
                if erc20Transaction["tokenSymbol"] not in tokenList:
                    numTokens += 1
                    tokenList.append(erc20Transaction["tokenSymbol"])
                    print(tokenList)
        return (inputs, outputs, numTokens)

    def isDoubleInputTokenTransaction(self, transaction):
        inputs, outputs, _  = self.getNumberOfInputAndOutputTokenTransactions(transaction)
        return inputs == 2 and outputs < 2

    def isDoubleOutputTokenTransaction(self, transaction):
        inputs, outputs, _ = self.getNumberOfInputAndOutputTokenTransactions(transaction)
        return outputs == 2 and inputs < 2

    def isAddedLiquidity(self, transaction):
        inputs, outputs, numTokens = self.getNumberOfInputAndOutputTokenTransactions(transaction)
        if inputs == 1 and outputs == 2 and numTokens == 3:
            return True
        return False

    def isRemovedLiquidity(self, transaction):
        inputs, outputs, numTokens = self.getNumberOfInputAndOutputTokenTransactions(transaction)
        if inputs == 2 and outputs == 1 and numTokens == 3:
            return True
        return False

    def isStakingCompound(self, transaction):
        # 2 Inputs and 1 Output (e.g. Cake - Cake Syrup: Cake (reward) in, Cake(reward) out, Sryup (in)
        inputs, outputs, numTokens = self.getNumberOfInputAndOutputTokenTransactions(transaction)
        if inputs == 2 and outputs == 1 and numTokens == 2:
            return True
        return False

    def getTransactions(self, erc20=False, internal=False):
        if erc20:
            return self.erc20Transactions
        elif internal:
            return self.internalTransactions
        else:
            return self.transactions

    def getTransactionsAsDict(self, erc20=False, internal=False):
        transactionList = []
        for transaction in self.getTransactions(erc20, internal):
            entry = {}
            value = int(transaction["value"])/1E18 if not erc20 else int(transaction["value"]) / (10**int(transaction["tokenDecimal"]))
            currency = "BNB" if not erc20 else transaction["tokenSymbol"]

            if transaction["from"] == self.address and value > 0:
                entry["category"] = "Transfer Out"
                entry["amountOut"] = value
                entry["currencyOut"] = currency
                # todo check for erc20 token with same txid, then its a swap! ###or: search in both output transactions fpr same id!!

            elif transaction["to"] == self.address and value > 0:
                entry["category"] = "Transfer In"
                entry["amountIn"] = value
                entry["currencyIn"] = currency
                # todo check for erc20 token with same txid, then its a swap!

            elif transaction["from"] == self.address and value == 0:
                # Check if an complimentary entry exists in the ERC20 transactions
                # Then skip, because fees are contained in that
                if not(erc20) and self.isTransactionInERC20Transactions(transaction):
                    continue
                entry["category"] = "Fees"
            elif transaction["to"] == self.address and value == 0:
                continue
            else:
                print(transaction)
                print(value)
                print(transaction["to"] == self.address)
                raise ("Unknown transaction!")

            entry["txId"] = transaction["hash"]
            entry["time"] = datetime.datetime.fromtimestamp(int(transaction["timeStamp"]), tz=timezone.utc)

            if not(erc20) and bool(int(transaction["isError"])):
                entry["category"] = "Loss"

            if erc20 and len(transactionList) > 0 and transactionList[-1]["txId"] == entry["txId"] and \
                    transactionList[-1]["category"] != entry["category"] and not(self.isAddedLiquidity(transaction)) \
                    and not(self.isRemovedLiquidity(transaction)):
                # Check that the currencies match (must be different in a trade)
                if (("amountIn" in entry and entry["amountIn"] > 0) and \
                    ("amountOut" in transactionList[-1] and transactionList[-1]["amountOut"] > 0) and
                    (entry["currencyIn"]!=transactionList[-1]["currencyOut"])) or \
                    (("amountOut" in entry and entry["amountOut"] > 0) and \
                     ("amountIn" in transactionList[-1] and transactionList[-1]["amountIn"] > 0) and
                     (entry["currencyOut"] != transactionList[-1]["currencyIn"])):

                    lastEntry = transactionList.pop()
                    entry = {**lastEntry, **entry} # combines both dict entries
                    entry["category"] = "Trade"

                # TODO: double transactions can also be compound + harvest ---> they are wrong now (trade + transfer in)

            ## Add liquidity = two output transactions
            #if erc20 and len(transactionList) > 0 and transactionList[-1]["txId"] == entry["txId"] and \
            #        transactionList[-1]["category"] == entry["category"] and entry["category"] == "Transfer Out":
            ##    # add another transaction
            #    print(entry["txId"])
            #    #entry["category"] = "Liquidity"
            #    #transactionList[-1]["category"] = "Liquidity"
            #    print("LIQUIDITY added")

            ## Remove liquidity
            #if erc20 and len(transactionList) > 0 and transactionList[-1]["txId"] == entry["txId"] and \
            #        transactionList[-1]["category"] == entry["category"] and entry["category"] == "Transfer in":
            ##    # add another transaction
            #    print(entry["txId"])
            #    #entry["category"] = "Liquidity"
            #    #transactionList[-1]["category"] = "Liquidity"
            #    print("LIQUIDITY removed")

            if entry["category"] != "Transfer In":
                entry["fee"] = int(transaction["gasUsed"]) * int(transaction["gasPrice"]) / 1E18
                entry["feeCurrency"] = "BNB"

            if erc20 and self.isAddedLiquidity(transaction):
                entry["category"] = "Added Liquidtiy"
                if len(transactionList) > 0 and transactionList[-1]["txId"] == entry["txId"]:
                    entry["fee"] = 0

            if erc20 and self.isRemovedLiquidity(transaction):
                entry["category"] = "Removed Liquidity"
                if len(transactionList) > 0 and transactionList[-1]["txId"] == entry["txId"]:
                    entry["fee"] = 0

            #if erc20 and self.isStakingCompound(transaction):
            #    entry["category"] = "Compound"
            #    if len(transactionList) > 0 and transactionList[-1]["txId"] == entry["txId"]:
            #        entry["fee"] = 0

            #if erc20 and "currencyOut" in entry and entry["currencyOut"].upper() == "CAKE-LP" and entry["category"]=="Tramsfer Out":
            #    entry["category"] = "Farm add"

            #if erc20 and entry["currencyIn"].upper() == "CAKE-LP":
            #    entry["category"] = "Farm remove"

            if internal:
                entry["note"] = "Internal Tx"

            transactionList.append(entry)

        return transactionList
    
    def getBalances(self):
        transactions = self.getAllTransactions()

        print("FINISHED FETCHING")

        print(transactions)

        assetList = []
        for transaction in transactions:
            if "currencyIn" in transaction and not(transaction["currencyIn"] in assetList) and transaction["currencyIn"] != "":
                assetList.append(transaction["currencyIn"])

        amountList = []
        for asset in assetList:
            elem = {}
            elem['currency'] = asset
            elem['amount'] = 0.0
            for transaction in transactions:
                if "currencyIn" in transaction and transaction["currencyIn"] == asset:
                    elem['amount'] += transaction["amountIn"]
                if "currencyOut" in transaction and transaction["currencyOut"] == asset:
                    elem['amount'] -= transaction["amountOut"]
                if "feeCurrency" in transaction and transaction["feeCurrency"] == asset:
                    elem['amount'] -= transaction["fee"]
            amountList.append(elem)

        return amountList

    # TODO: multiple inupts:  (beefy barn for example)
    # TODO: multiple outputs: wrong fee (doubled fee)

if __name__ == "__main__":
    print("main")
    testAcc = BscTransactions("0x28D736A96649F1ad228865bc2a0FF10Ec663a0b0")
    for asset in testAcc.getBalances():
        print("%s : %.2f\n" % (asset["currency"],asset["amount"]) )
    