import hashlib
from pycoin import ecdsa, encoding
import os
import codecs
for i in range(10):
    rand = codecs.encode(os.urandom(32), 'hex').decode()
    secret_exponent= int('0x'+rand, 0)
    print ('WIF: ' + encoding.secret_exponent_to_wif(secret_exponent, compressed=False))
    public_pair = ecdsa.public_pair_for_secret_exponent(ecdsa.secp256k1.generator_secp256k1, secret_exponent)
    hash160 = encoding.public_pair_to_hash160_sec(public_pair, compressed=True)
    print('Bitcoin address: %s' % encoding.hash160_sec_to_bitcoin_address(hash160))