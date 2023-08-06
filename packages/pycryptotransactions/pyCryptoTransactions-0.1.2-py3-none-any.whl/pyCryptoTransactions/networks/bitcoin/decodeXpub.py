#from btctools import Xpub
from cryptotools.BTC import Xpub, Address
import cryptotools
import requests
import datetime

#https://github.com/mcdallas/cryptotools
#https://bitcoin.stackexchange.com/questions/109981/derive-segwit-addresses-from-xpub-or-zpub-using-python
#https://bitcoin.stackexchange.com/questions/60565/is-it-possible-to-use-xpub-address-to-monitor-balance-from-previously-generated

#Learn: https://learnmeabitcoin.com/technical/derivation-paths


########################################

################ BITCOIN ################

#extended = Xpub.decode('xpub6C2zcaw8NCGbNwEo5KGPBYzNj6UpfspemmAfgsgxWTRvNPrXR6Sh9pvZvfNTjHaZ8mVPZjxMgi8RbCgecGSecU64agjh9uxQMXwPkxPf9bP')
extended = Xpub.decode('xpub6DBEa6eSZXgZ6GAkiyoWW5QEVKoU5oQ3geRyXfwmYTx75u5sMcB3LMEs5wSjKhPazrzFG1as4cu9Lgb53j1NRujueWqpn7GgmjkYJm9hs63')
print(extended.type)
#xpub6CEJ63Dk5YFhWhFraNVYz36VUhgQy1ed6j5gRDyJyJuWjM33KyDfS4hSWAa6CVUF7g3VtCqeEHs1TV1tgyYyWLvT4566DJYDbfG59DM3SGm #segwit
#xpub6DBEa6eSZXgZ6GAkiyoWW5QEVKoU5oQ3geRyXfwmYTx75u5sMcB3LMEs5wSjKhPazrzFG1as4cu9Lgb53j1NRujueWqpn7GgmjkYJm9hs63 #legacy
child = extended/0/0
#0/x = Receiving = 0 - Addresses that we will give out to people for receiving payments.
#1/x = Change = 1 - Addresses we use for sending change back to ourselves when we make transactions.

print(child)
print(child.key.to_address('P2WPKH')) #native segwite # bip84
print(child.key.to_address('P2PKH')) #Pay-to-Pubkey Hash - legacy  # bip44
#print(child.key.to_address('P2SH')) #segwit
print(child.key.to_address('P2WPKH-P2SH')) #segwit

curAddress = child.key.to_address('P2WPKH-P2SH')
address = Address(curAddress)
print(address.balance())
print(address.utxos)

##########################################

#1KCECbqEiHmdeLnPaBDc3J7h4upguV7M9S 



#Test:MULiubAyQSZNDgvvtj7q5D64vMbCCJfafP
print("###")

## doesnt work
def getbalance(address):
  response = requests.get("https://blockchain.info/rawaddr/%s" % address)
  if response.status_code != 200:
    return None
  return response.json()["final_balance"]
  
def listtransactions(address):
  response = requests.get("https://blockchain.info/rawaddr/%s" % address)
  if response.status_code != 200:
    return None
  for tx in response.json()["txs"]:
      #print(tx["time"])
      tx_timestr = datetime.datetime.fromtimestamp(tx["time"])
      tx_amount = satoshis_to_btc(tx["result"])
      print("Transaction (%s): %s %s" % (tx_timestr, "unknown type", tx_amount))
    
  return response.json()

def satoshis_to_btc(value):
  return float(float(value) / 10**8)


print(getbalance(curAddress))
listtransactions(curAddress)




####