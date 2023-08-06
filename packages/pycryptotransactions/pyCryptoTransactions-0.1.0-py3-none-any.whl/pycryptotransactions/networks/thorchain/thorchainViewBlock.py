#https://midgard.thorchain.info/v2/actions?offset=0&limit=10&address=thor1khjg7et54q4zzef62ud0z8ps0ypnf69g5hfxjc

#https://thornode.thorchain.info/bank/balances/thor1khjg7et54q4zzef62ud0z8ps0ypnf69g5hfxjc

#https://midgard.thorchain.info/v2/member/thor1khjg7et54q4zzef62ud0z8ps0ypnf69g5hfxjc --> all pools
#https://viewblock.io/thorchain/address/thor12dpps82a5a2zmzdvq74rjunfjh2szykgcr9anw?page=1

from datetime import datetime
import pytz as timezone
from decimal import Decimal
from copy import deepcopy

from pyCryptoTransactions.Transaction import Position, Transaction,TransactionList, Fee
from pyCryptoTransactions.Importer import Importer
import time
import datetime
import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import re, json

class ThorchainViewBlockImporter(Importer):
    def __init__(self, address):
        super().__init__()
        self.address = address
        self._apiAdress = 'https://viewblock.io/thorchain/address/' + self.address
        #self._initRequest()

        self.rawTxs = None

        self.denominator = Decimal(int(1E8))
        self.chain = "thorchain"
        self.unit = "RUNE"
    
    def _request(self, path, apiAdress=None, **params):
        if apiAdress == None:
                apiAdress = self._apiAdress
        try:
            # NOTE: Session doesn't work here, some parts are missing
            response = requests.get(apiAdress + path)
            #response = self.session.get(apiAdress + path, params=params)
            if response.status_code != 200:
                raise("Error in the request")
            text = response.text
            r = re.search('window\.\_\_INITIAL\_STATE\_\_ =(.+)', text)
            d = json.loads(r.group(1))
            return d["main"]["address"]["thorchain"]["map"][self.address]
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)
            raise("Connection Error")
    
    def _getRawTransactions(self, page=0, **kwargs):
        values = {}
        values['page'] = page
        for k in kwargs:
            if kwargs[k] is not None:
                values[k] = kwargs[k]
        return self._request('/', **values)

    def _getAllRawTransactions(self):
        return NotImplemented

    def getTransactions(self, time=None) -> TransactionList:
        txsRaw = self._getRawTransactions() #todo:replace with getAllRawTransactions
        for tx in txsRaw["txs"]["docs"]:
            time = datetime.datetime.fromtimestamp(int(tx["timestamp"])/1E3, tz=timezone.utc)
            txHash = tx["hash"]
            fee = Fee( Decimal(tx["fee"])/self.denominator, self.unit)
            memo = '_'.join(tx["extra"]["thorMemos"])
            category = '_'.join(tx["extra"]["thorLabels"])
            #status = tx["status"] == "success"
            t = Transaction(dateTime=time, fee=fee, txHash=txHash, category=category)
            t.memo = memo

            outgoing = False
            ingoing = False
            for transfer in tx["transfers"]:
                amount = Decimal(int(0))
                for fromTransfer in transfer["from"]:
                    if fromTransfer["address"] == self.address:
                        outgoing = True
                        t.fromAddress = self.address
                    t.fromAddress = fromTransfer["address"] if t.fromAddress is not None or t.fromAddress != "" else t.fromAddress
                        # amount seems to be always in the "to" transfer --> TODO: Check if this is alway true!
                for toTransfer in transfer["to"]:
                    if toTransfer["address"] == self.address:
                        ingoing = True
                        t.toAddress = self.address
                    t.toAddress = fromTransfer["address"] if t.toAddress is not None or t.toAddress != "" else t.toAddress
                    if amount != 0:
                        raise ValueError("Amount was already set once! Check implementation and API (changes)")
                    amount += Decimal(toTransfer["value"])/self.denominator
                
            # Thorchain is just RUNE for now, so there can't be in and out rune to our address at the same time
            if outgoing and ingoing:
                raise Exception("Both in and out going transaction detected! Check implementation and API (changes)!")
            
            if outgoing:
                t.posOut = Position(amount, "RUNE")
            elif ingoing:
                t.posIn = Position(amount, "RUNE")
                t.fee.amount = 0
            else:
                print("Neither in nor out transaction detected!")
            
            #if tx["extra"]["thorOps"]["hasOps"]:
            #    if ingoing:
            #        t.blockHeight = tx["extra"]["thorOps"]["outs"][0]["blockHeight"] #thorchain outs are our ins #TODO: can there be more than 1?
            #    elif outgoing:
            #        t.blockHeight = tx["extra"]["thorOps"]["ins"][0]["blockHeight"]
                
            self.txList.append(t)
        return self.txList