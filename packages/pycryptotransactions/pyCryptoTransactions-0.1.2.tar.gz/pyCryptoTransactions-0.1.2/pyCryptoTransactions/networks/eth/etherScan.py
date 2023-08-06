from etherscan.accounts import Account
from etherscan.client import EmptyResponse
import datetime
from django.utils import timezone
from ..portfolioConfig import ETHERSCAN_APIKEY

class EtherTransactions():
    def __init__(self,  etherAccountAddress, apiKey=ETHERSCAN_APIKEY):
        self.apiKey = apiKey
        self.address = etherAccountAddress.lower()
        self.etherScanAccountApi = Account(address=etherAccountAddress, api_key=self.apiKey)
        self.transactions = []
        self.erc20Transactions = []
        self.internalTransactions = []

    def update(self):
        try:
            self.transactions = self.etherScanAccountApi.get_transaction_page()
        except EmptyResponse:
            self.transactions = []
        try:
            self.erc20Transactions = self.etherScanAccountApi.get_transaction_page(erc20=True)
        except EmptyResponse:
            self.erc20Transactions = []
        try:
            self.internalTransactions = self.etherScanAccountApi.get_transaction_page(erc20=False, internal=True)
        except EmptyResponse:
            self.internalTransactions = []

    def getAllTransactions(self, startTime=None):
        self.update()
        normalTransactions = self.getTransactionsAsDict(erc20=False)
        erc20TransActions = self.getTransactionsAsDict(erc20=True)
        internalTransactions = self.getTransactionsAsDict(erc20=False, internal=True)
        allTransactions = normalTransactions + erc20TransActions + internalTransactions

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
                        erc20TransAction["category"] = "Swap"
                        erc20TransAction["amountIn"] = normalTransaction["amountIn"]
                        erc20TransAction["currencyOut"] = normalTransaction["currencyIn"]
                        allTransactions.remove(normalTransaction)

        # Remove elements that are before startTime
        # for transaction in allTransactions:

        return allTransactions

    def isTransactionInERC20Transactions(self, transaction):
        for erc20Transaction in self.erc20Transactions:
            if erc20Transaction["hash"] == transaction["hash"]:
                return True
        return False

    def getTransactions(self,erc20=False, internal=False):
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
            currency = "ETH" if not erc20 else transaction["tokenSymbol"]

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
                    transactionList[-1]["category"] != entry["category"]:
                lastEntry = transactionList.pop()
                entry = {**lastEntry, **entry}
                entry["category"] = "Trade"

            if entry["category"] != "Transfer In":
                entry["fee"] = int(transaction["gasUsed"]) * int(transaction["gasPrice"]) / 1E18
                entry["feeCurrency"] = "ETH"

            if internal:
                entry["note"] = "Internal Tx"

            transactionList.append(entry)

        return transactionList
