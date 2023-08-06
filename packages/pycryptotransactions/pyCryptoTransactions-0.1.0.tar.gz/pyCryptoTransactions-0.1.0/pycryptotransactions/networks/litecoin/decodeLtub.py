from cryptotools.BTC import Xpub
import cryptotools
import requests
import datetime

#Change bitcoin network settings to litecoin
#https://bitcoin.stackexchange.com/questions/62781/litecoin-constants-and-prefixes/80355#80355
cryptotools.BTC.network.main["extended_pub"]["P2PKH"] = b'\x01\x9d\xa4\x62' #0x019DA462 #Ltub
cryptotools.BTC.network.main["hrp"] = 'ltc' #0x019DA462 #Ltub
cryptotools.BTC.network.main["keyhash"] = b'\x30'
cryptotools.BTC.network.main["scripthash"] = b'\x32' #new M-address
cryptotools.BTC.network.main["wif"] = b'\x36' #not important?

segwitXpub = 'Ltub2ZYYmNuYZRAyCFNp8LAPEwxnRG9jkx4qmmPDwTfQNe19JgURHxAL1WjoMP24ZP8fxZafCTd8SBR9acr9KWjWmM3rtyFsRfQf3dk3cK2hgV5'
legacyXpub = 'Ltub2Z1YoRfU7gavCJ5ChwGNAnmcpDK35wzCRAB2mstyVjV7ShQGnizKTyL6kFNhK4KNuWypAYvAS534LFowXrFRPLQRacRBemKrrAWCzuPEe4o'
extended = Xpub.decode(legacyXpub)
child = extended/0/0
print(child.key.to_address('P2WPKH')) #native segwite # bip84
print(child.key.to_address('P2PKH')) #Pay-to-Pubkey Hash - legacy  # bip44
print(child.key.to_address('P2WPKH-P2SH')) #segwit

#LbNrLRMKNG68zHeNnDdMotK8Vr2jLz3bej
#add from legacy xpub wrong (decode assumes segwit?)



from cryptotools.BTC import Xprv
m = Xprv.from_mnemonic('bench auction print immense castle slide tip pill evolve abandon canvas ugly')
M = m.to_xpub()
print(M)
print(M.encode())
print(M.address('P2PKH'))
print((m/0./0).to_xpub())
print((m/0./0).address('P2PKH'))  # bip44)
print((m/0./0).to_xpub().encode())
#(m/123/456).to_xpub()
#(m/44./0./0./0/0).address('P2PKH')