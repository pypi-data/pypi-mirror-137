def getTransactions(self, time=None) -> TransactionList:
        #return super().getTransactions(time=time)
        self.rawTxs = self._getRawTransactions()

        for tx in self.rawTxs:
            time = datetime.strptime(tx["header"]["timestamp"],"%Y-%m-%dT%H:%M:%SZ")
            height = tx["data"]["height"]
            txHash = tx["data"]["txhash"]

            t = Transaction(dateTime=time, txHash=txHash, blockHeight=height)

            #1. Fee
            #if tx["header"]["chain_id"] == "cosmoshub-3":
            fee = tx["data"]["tx"]["auth_info"]["fee"]["amount"][0]["amount"] if "auth_info" in tx["data"]["tx"] else tx["data"]["tx"]["value"]["fee"]["amount"][0]["amount"]
            feeCurrency = tx["data"]["tx"]["auth_info"]["fee"]["amount"][0]["denom"] if "auth_info" in tx["data"]["tx"] else tx["data"]["tx"]["value"]["fee"]["amount"][0]["denom"]
            t.fee = Fee(Decimal(fee)/self.denominator, self.getSymbol(feeCurrency) )

            #2.Memo
            memo = tx["data"]["tx"]["value"]["memo"] if tx["header"]["chain_id"] == "cosmoshub-3" else tx["data"]["tx"]["body"]["memo"]
            t.memo = memo

            #only add fee once for every log
            feeAdded = False 
            for log in tx["data"]["logs"]:
                tmp = deepcopy(t)
                addTransaction = False
                events = log["events"] #todo: check --> no logs for failed txs
                delegated = False
                rewards = False
                for event in events:
                    if event["type"] == "delegate":
                        #tmp.note = "Delegated"
                        for attr in event["attributes"]:
                            print(attr["key"])
                            if attr["key"] == "amount":
                                print("FOUND")
                                tmp.note = "Delegated {}ATOM".format(Decimal(attr["value"])/self.denominator)
                        addTransaction = True
                        delegated = True
                    if event["type"] == "withdraw_rewards":
                        tmp.category = "Staking"
                        rewards = True
                    if event["type"] == "transfer":
                        attrs = event["attributes"]
                        recipientIdx = None
                        senderIdx = None
                        amountIdx = None
                        for idx,attr in enumerate(attrs):
                            if attr["key"] == "recipient":
                                recipientIdx = idx
                            if attr["key"] == "sender":
                                senderIdx = idx
                            if attr["key"] == "amount":
                                amountIdx = idx
                        
                        # We need at least a sender or recipient and an amount
                        assert(recipientIdx!=None or senderIdx!=None)
                        assert(amountIdx!=None)
                        
                        if recipientIdx is not None:
                            tmp.toAddress = attrs[recipientIdx]["value"]
                        if senderIdx is not None:
                            tmp.fromAddress = attrs[senderIdx]["value"]
                        
                        # parse amount
                        amount = attrs[amountIdx]["value"]
                        number, unit = self._parseAmount(amount)

                        # check for ibc token
                        if unit[0:4] == "ibc/":
                            unit, decimal = self.getIbcTokenSymbolFromIBCTokenHash(unit[4:])
                        else:
                            unit = self.getSymbol(unit)
                            decimal = self.denominator

                        #check for in or out transaction
                        if tmp.fromAddress == self.address:
                            tmp.posOut = Position(Decimal(number)/Decimal(decimal), unit)
                            addTransaction = True
                        elif tmp.toAddress == self.address:
                            tmp.posIn = Position(Decimal(number)/Decimal(decimal), unit)
                            addTransaction = True

                # Delete Fee for incoming txs or if it was already added for another transaction of the same tx hash
                if (tmp.posIn.amount != 0 and not(delegated) and not(rewards)) or feeAdded:
                    tmp.fee.amount = 0
                elif tmp.posIn.amount != 0 and delegated:
                    tmp.note += " (+auto claim reward)"
                    tmp.category = "Staking"
                    feeAdded = True
                else:
                    feeAdded = True

                if addTransaction:
                    self.txList.append(tmp)

        return self.txList