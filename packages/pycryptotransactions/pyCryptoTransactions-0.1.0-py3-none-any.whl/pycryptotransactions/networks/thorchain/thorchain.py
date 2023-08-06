#https://midgard.thorchain.info/v2/actions?offset=0&limit=10&address=thor1khjg7et54q4zzef62ud0z8ps0ypnf69g5hfxjc

#https://thornode.thorchain.info/bank/balances/thor1khjg7et54q4zzef62ud0z8ps0ypnf69g5hfxjc

#https://midgard.thorchain.info/v2/member/thor1khjg7et54q4zzef62ud0z8ps0ypnf69g5hfxjc --> all pools

from datetime import datetime
import pytz as timezone
from decimal import Decimal
from copy import deepcopy

from pyCryptoTransactions.Transaction import Position, Transaction,TransactionList, Fee
from pyCryptoTransactions.Importer import Importer
import time
import datetime

class ThorchainImporter(Importer):
    def __init__(self, address):
        super().__init__()
        self._apiAdress = 'https://midgard.thorchain.info/v2/actions'
        self.balanceApiAdress = "https://thornode.thorchain.info/bank/balances/"
        self._initRequest()

        self.rawTxs = None
        self.address = address

        self.denominator = Decimal(int(1E8))
        self.chain = "thorchain"
        self.unit = "RUNE"
    
    def _getRawTransactions(self, offset=0, limit=10, **kwargs):
        values = {}
        values['limit'] = limit
        values['offset'] = offset
        values['address'] = self.address
        for k in kwargs:
            if kwargs[k] is not None:
                values[k] = kwargs[k]
        return self._request('/', **values)

    def _getAllRawTransactions(self):
        return NotImplemented

    def getTransactions(self, time=None) -> TransactionList:
        txsRaw = self._getRawTransactions() #todo:replace with getAllRawTransactions

        for tx in txsRaw["actions"]:
            time = datetime.datetime.fromtimestamp(int(tx["date"])/1E9,tz=timezone.utc)
            height = tx["height"]
            category = tx["type"]
            status = tx["status"] == "success"
            t = Transaction(dateTime=time, blockHeight=height, category=category)
            if "in" in tx:
                for txOut in tx["in"]: #thorchain api in means actually outgoing tx from us
                    if txOut["address"] == self.address:
                        t.fromAddress = self.address
                        for coin in txOut["coins"]:
                            tmp = deepcopy(t)
                            tmp.txHash = txOut["txID"]
                            tmp.posOut = Position(Decimal(coin["amount"])/self.denominator, coin["asset"].split(".")[1].split('-')[0])
                            if tmp.category == "addLiquidity":
                                tmp.fee = Fee(Decimal("0.02"),"RUNE")
                            self.txList.append(tmp)
            if "out" in tx:
                for txIn in tx["out"]: #thorchain api out means actually ingoging tx to us
                    if txIn["address"] == self.address:
                        t.toAddress = self.address
                        for coin in txIn["coins"]:
                            tmp = deepcopy(t)
                            tmp.txHash = txIn["txID"]
                            tmp.posIn = Position(Decimal(coin["amount"])/self.denominator, coin["asset"].split(".")[1].split('-')[0])
                            self.txList.append(tmp)
        return self.txList