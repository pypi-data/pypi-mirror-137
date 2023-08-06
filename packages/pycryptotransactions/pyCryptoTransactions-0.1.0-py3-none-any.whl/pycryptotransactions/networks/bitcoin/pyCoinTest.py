from pycoin.symbols.btc import network
from pycoin.networks.registry import network_for_netcode
import pycoin

key = network.parse.bip32("xprv9s21ZrQH143K31AgNK5pyVvW23gHnkBq2wh5aEk6g1s496M"
      "8ZMjxncCKZKgb5jZoY5eSJMJ2Vbyvi2hbmQnCuHBujZ2WXGTux1X2k9Krdtq")
print(key.hwif(as_private=1))
print(key.hwif())
print(key.wif())
print(key.sec())
print(key.address())

key = network.parse.bip32("xpub6DBEa6eSZXgZ6GAkiyoWW5QEVKoU5oQ3geRyXfwmYTx75u5sMcB3LMEs5wSjKhPazrzFG1as4cu9Lgb53j1NRujueWqpn7GgmjkYJm9hs63")
print(key.address())

key = network.parse.bip32_pub("xpub6DBEa6eSZXgZ6GAkiyoWW5QEVKoU5oQ3geRyXfwmYTx75u5sMcB3LMEs5wSjKhPazrzFG1as4cu9Lgb53j1NRujueWqpn7GgmjkYJm9hs63")
print(key.address()) #legacy
print(key.hash160()) #legacy
print(key.ku_output_for_address())

xpub = network.parse.address("xpub6C2zcaw8NCGbNwEo5KGPBYzNj6UpfspemmAfgsgxWTRvNPrXR6Sh9pvZvfNTjHaZ8mVPZjxMgi8RbCgecGSecU64agjh9uxQMXwPkxPf9bP")
print("11")
print(xpub)

#legacy xpub (blockchain info)
key = network.parse("xpub6DBEa6eSZXgZ6GAkiyoWW5QEVKoU5oQ3geRyXfwmYTx75u5sMcB3LMEs5wSjKhPazrzFG1as4cu9Lgb53j1NRujueWqpn7GgmjkYJm9hs63")
print(key.address())
print(key.address(is_compressed=False))
subkey = key.subkey_for_path("0")
print(subkey.address())
subkey = key.subkey_for_path("0/0") #---->richtig
print(subkey.address())
subkey = key.subkey_for_path("1/0") #---->richtig
print(subkey.address())

key = network.parse("xpub661MyMwAqRbcGcWc7LfVdJnRUR2M9Qtp5675dw78aFLgjULMnniKvU4PhBve1gMHuVdUDZiykxdb2xxcqbxkZKNDssKwPZNJrJeP4j9z5fv")
subkey = key.subkey_for_path("0/0") 
print(subkey.address())

print("segwit")
#segwit
key = network.parse("xpub6C2zcaw8NCGbNwEo5KGPBYzNj6UpfspemmAfgsgxWTRvNPrXR6Sh9pvZvfNTjHaZ8mVPZjxMgi8RbCgecGSecU64agjh9uxQMXwPkxPf9bP")
#nachfolgender geht, benoetigt aber conversion https://jlopp.github.io/xpub-converter/
#key = network.parse("ypub6WsFvFc3Wsp5EERuug41Pe5su4dGcVp9gsgtUGaqtTooRVfkfkcFmtahwsL3jCEUYQcCKDYv9NUyUVJDKxrfQhmfT2S7jpmtdG139Upvgub")
print(key.address())
print(key.address(is_compressed=False))
subkey = key.subkey_for_path("0")
print(subkey.address())
subkey = key.subkey_for_path("0/0") 
print(subkey.address())
subkey = key.subkey_for_path("1/0") 
print(subkey.address())
#39Abxbt4vs78qfiUw8wDd1cGr3Rg7wURaK

subkey = key.subkey_for_path("0/0") 
print("Native segwit")
print(network.address.for_p2pkh_wit(subkey.hash160(is_compressed=True)))
#Segwit:
print("Segwit")
print(network.address.for_p2sh(subkey.hash160(is_compressed=True)))

## From contract
script = network.contract.for_p2pkh_wit(subkey.hash160(is_compressed=True))
print(network.address.for_p2s(script)) #--->RICHTIG (#P2WPKH in P2SH / ypub)
#-->pycoin/key/BIP49Node.py

#Geht nicht:
#key = network.parse.bip49("xpub6C2zcaw8NCGbNwEo5KGPBYzNj6UpfspemmAfgsgxWTRvNPrXR6Sh9pvZvfNTjHaZ8mVPZjxMgi8RbCgecGSecU64agjh9uxQMXwPkxPf9bP")
#subkey = key.subkey_for_path("0/0") 
#print(subkey.address())

#pycoin.networks._bip49_pub_prefix = "xpub"
#key = network.parse.bip49_pub("xpub6C2zcaw8NCGbNwEo5KGPBYzNj6UpfspemmAfgsgxWTRvNPrXR6Sh9pvZvfNTjHaZ8mVPZjxMgi8RbCgecGSecU64agjh9uxQMXwPkxPf9bP")
#print(key.subkey_for_path("1/0").address())

##WORKS:
#~/C/crypto-/networks/bitcoin ❯ ku xpub6DBEa6eSZXgZ6GAkiyoWW5QEVKoU5oQ3geRyXfwmYTx75u5sMcB3LMEs5wSjKhPazrzFG1as4cu9Lgb53j1NRujueWqpn7GgmjkYJm9hs63 -s 0/0-10 -a
#ku xpub6DBEa6eSZXgZ6GAkiyoWW5QEVKoU5oQ3geRyXfwmYTx75u5sMcB3LMEs5wSjKhPazrzFG1as4cu9Lgb53j1NRujueWqpn7GgmjkYJm9hs63 -s 1/0-10 -a


## Litecoin from xpub
print("assdasd\n")
from pycoin.networks.bitcoinish import create_bitcoinish_network
network = create_bitcoinish_network(
    network_name="Litecoin", symbol="LTC", subnet_name="mainnet",
    wif_prefix_hex="b0", sec_prefix="LTCSEC:", address_prefix_hex="30", pay_to_script_prefix_hex="32",
    bip32_prv_prefix_hex="019d9cfe", bip32_pub_prefix_hex="0488B21E", bech32_hrp="ltc") ##bip32_pub_prefix_hex from bitcoin
pub = "xpub661MyMwAqRbcFrfZqAH8d94hEQKBitWTBMNmshSZiVrydCE3dFRt8C6TwnufWTZjFGgEfoDPJTVGdbFSJFYYpZDRonDrtpGPyMkcGXhpmFX"
key = network.parse(pub)
print(key.subkey_for_path("0/0").address()) #-->stimmt


#litecoin
print("\nLitecoin")
network = network_for_netcode("LTC")
pub = "Ltub2Z1YoRfU7gavCJ5ChwGNAnmcpDK35wzCRAB2mstyVjV7ShQGnizKTyL6kFNhK4KNuWypAYvAS534LFowXrFRPLQRacRBemKrrAWCzuPEe4o"
key = network.parse.bip32(pub)
print(key.subkey_for_path("0/0").address()) #-->stimmt
#LbNrLRMKNG68zHeNnDdMotK8Vr2jLz3bej

#segwit
pub = "Ltub2ZYYmNuYZRAyCFNp8LAPEwxnRG9jkx4qmmPDwTfQNe19JgURHxAL1WjoMP24ZP8fxZafCTd8SBR9acr9KWjWmM3rtyFsRfQf3dk3cK2hgV5"
key = network.parse(pub)
subkey = key.subkey_for_path("0/0") 
script = network.contract.for_p2pkh_wit(subkey.hash160(is_compressed=True)) #xpub as ypub
print(network.address.for_p2s(script)) #--->stimmt
#MULiubAyQSZNDgvvtj7q5D64vMbCCJfafP


#########TESTS
#mobj = pycoin.mnemonic.Mnemonic("english")
#seed = mobj.to_seed("bench auction print immense castle slide tip pill evolve abandon canvas ugly")
#key = network.keys.bip39_seed("99b269aecb097d51961c086e2c6baa595d9e939e156709871352c737b91f55806d3ec11c27251caeec650215e0a02da4ca4a5e4f7659290060dc37ef2a0a1bc3")
#subkey = key.subkey_for_path("44/2H/0H/0/0")
#print(subkey.address)

# Loafwallet 
pub = "Ltub2XuZ5AKXavgGqmSegPmhyZ5BMS4FJAZoCweSRCUDBTffni8DuNfJxu8BjqinjSqKtpE1ED8mCNgKt2Y3gQKaTEup5TFdfjv9NXYMxMEvXeg"
key = network.parse.bip32(pub)
print(key.subkey_for_path("0").address()) #--->das ist er
print(key.address())

pub = "Ltub2Vf5gKHAw7d1hUfLu3iaLMvzkND99PoE2tr2duBdDvRMyUGG7zdaURJjGZGtFRLnzNEL1oSijkTfPfk86M3FkWE5p2zbAoHrsQ7vEfeyoEk"
key = network.parse.bip32(pub)
print(key.subkey_for_path("0/0").address()) #----> YES. LOAFWALLET: Derivation Path m/0'/ on https://iancoleman.io/bip39/ (Tab bip32)


#Electrum LTC: xpub661MyMwAqRbcFrfZqAH8d94hEQKBitWTBMNmshSZiVrydCE3dFRt8C6TwnufWTZjFGgEfoDPJTVGdbFSJFYYpZDRonDrtpGPyMkcGXhpmFX
#pub = "xpub661MyMwAqRbcFrfZqAH8d94hEQKBitWTBMNmshSZiVrydCE3dFRt8C6TwnufWTZjFGgEfoDPJTVGdbFSJFYYpZDRonDrtpGPyMkcGXhpmFX"
#key = network.parse(pub)
#print(key.subkey_for_path("0/0").address()) 
#print(key.address())

print(network.symbol)