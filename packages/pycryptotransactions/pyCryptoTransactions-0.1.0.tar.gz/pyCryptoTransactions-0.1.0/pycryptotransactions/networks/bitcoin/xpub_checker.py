#!/usr/bin/python

import pycoin.key
import sys
import requests
import json
import datetime
from pycoin.key.Key import Key

def getbalance(address):
  response = requests.get("https://bitaps.com/api/address/%s" % address)
  if response.status_code != 200:
    return None
  return response.json()
  
def listtransactions(address):
  response = requests.get("https://bitaps.com/api/address/transactions/%s" % address)
  if response.status_code != 200:
    return None
  return response.json()

def satoshis_to_btc(value):
  return float(float(value) / 10**8)

def probe_used_addresses(xpub, account_type):
  xpub_subkey = xpub.subkey(account_type)
  index = 0
  while True:
    addr = xpub_subkey.subkey(index).bitcoin_address()
    print("Type %d (%d): %s" % (account_type, index, addr))
    
    # Report balance data
    balancedata = getbalance(addr)
    balance = balancedata['confirmed_balance']
    balance_btc = satoshis_to_btc(balance)
    print("  Balance: %s" % balance_btc)
    
    # List transactions, if any...
    transactions = listtransactions(addr)
    if transactions != None:
      for tx in transactions:
        tx_time = datetime.datetime.fromtimestamp(float(tx[0]))
        tx_hash = tx[1]
        tx_data = tx[2]
        tx_type = tx[3]
        tx_status = tx[4]
        tx_confirmations = tx[5]
        tx_block = tx[6]
        tx_amount = satoshis_to_btc(tx[7])
        tx_timestr = tx_time.isoformat()
        print("    Transaction (%s): %s %s" % (tx_timestr, tx_type, tx_amount))

    print("")
    
    if transactions == None:
        break
    index += 1

def main():
  from pycoin.symbols.btc import network
  key = network.parse.bip32("xprv9s21ZrQH143K31AgNK5pyVvW23gHnkBq2wh5aEk6g1s496M"
      "8ZMjxncCKZKgb5jZoY5eSJMJ2Vbyvi2hbmQnCuHBujZ2WXGTux1X2k9Krdtq")
  print(key.hwif(as_private=1))
  print(key.hwif())
  print(key.wif())
  print(key.sec())
  print(key.address())

  xpub = Key.from_text(sys.argv[1])
  probe_used_addresses(xpub, 0)
  probe_used_addresses(xpub, 1)

main()
