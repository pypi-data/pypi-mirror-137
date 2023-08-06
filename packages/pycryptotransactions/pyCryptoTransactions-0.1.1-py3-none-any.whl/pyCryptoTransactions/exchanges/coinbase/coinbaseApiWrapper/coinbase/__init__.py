from .CoinbaseAPIKeyAuthentication import CoinbaseAPIKeyAuthentication
from .CoinbaseOAuth import CoinbaseOAuth
from .CoinbaseOAuthAuthentication import CoinbaseOAuthAuthentication
from .CoinbaseRPC import CoinbaseRPC
from .error import CoinbaseAPIException
from .error import CoinbaseException
class Coinbase(object):
    '''
    Manages all data and interactions with the Coinbase API.
    '''

    @staticmethod
    def with_api_key(key, secret, nonce=None):
        return Coinbase(
                CoinbaseAPIKeyAuthentication(
                    key, secret),
                nonce)

    @staticmethod
    def with_oauth(access_token, refresh_token):
        return Coinbase(
                CoinbaseOAuthAuthentication(
                    access_token, refresh_token))

    def __init__(self, authentication, nonce=None):
        self.__authentication = authentication
        self.__rpc = CoinbaseRPC(self.__authentication, nonce)

    def delete(self, path, params=None):
        return self.__rpc.request('DELETE', path, params)

    def get(self, path, params=None):
        return self.__rpc.request('GET', path, params)

    def post(self, path, params=None):
        return self.__rpc.request('POST', path, params)

    def put(self, path, params=None):
        return self.__rpc.request('PUT', path, params)