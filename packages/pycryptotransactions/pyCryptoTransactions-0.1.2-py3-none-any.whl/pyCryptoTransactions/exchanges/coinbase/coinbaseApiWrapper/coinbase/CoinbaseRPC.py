from .CoinbaseAPIKeyAuthentication import CoinbaseAPIKeyAuthentication
from .CoinbaseOAuthAuthentication import CoinbaseOAuthAuthentication
from .error import CoinbaseAPIException

import hashlib
import hmac
import json
import requests
import time
import urllib.parse
class CoinbaseRPC(object):
    '''
    Abstracts functionality for executing remote procedure calls.
    '''
    
    COINBASE_API_BASE = 'https://api.coinbase.com/'
    API_VERSION = 2
    COINBASE_API = COINBASE_API_BASE + 'v' + str(API_VERSION)
    def __init__(self, authentication, nonce=None):
        self.__authentication = authentication
        self.__nonce = None


    def request(self, method, url, params=None):
        url = self.COINBASE_API + url

        method = method.lower()
        if method == 'get' or method == 'delete':
            if params is not None:
                url += '?' + urllib.parse.urlencode(params)
        else:
            params = json.dumps(params)

        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'CoinbasePython3/v2'
        }

        auth = self.__authentication.get_data()

        if isinstance(self.__authentication, CoinbaseOAuthAuthentication):
            headers['Authorization'] = 'Bearer ' + auth['access_token']
        elif isinstance(self.__authentication, CoinbaseAPIKeyAuthentication):
            if self.__nonce is None:
                self.__nonce = int(time.time() * 1e6)
            message = str(self.__nonce) + url

            if method == 'post' or method == 'put':
                if params is not None:
                    message += params

            signature = \
                hmac.new(
                    auth['api_secret'].encode(),
                    message.encode(),
                    hashlib.sha256) \
                .hexdigest()

            headers['CB-ACCESS-KEY'] = auth['api_key']
            headers['CB-ACCESS-SIGN'] = signature
            headers['CB-ACCESS-TIMESTAMP'] = str(self.__nonce)
            headers['CB-VERSION'] = '2021-12-25'
            headers['Accept'] = 'application/json'
        else:
            raise CoinbaseAPIException('Invalid authentication mechanism')

        #debug: print(f"{method} {url} {headers}")
        if method == 'get':
            request = requests.get(url, headers=headers)
        elif method == 'delete':
            request = requests.delete(url, headers=headers)
        elif method == 'post':
            request = requests.post(url, data=params, headers=headers)
        elif method == 'put':
            request = requests.put(url, data=params, headers=headers)

        if request.status_code != 200:
            raise CoinbaseAPIException(
                    'Status Code ' + str(request.status_code),
                    request.status_code,
                    request.content.decode())

        content = json.loads(request.content.decode())
        if content is None or len(content) == 0:
            raise CoinbaseAPIException(
                    'Invalid response body',
                    request.status_code,
                    request.content.decode())

        if 'error' in content:
            raise CoinbaseAPIException(
                    content['error'],
                    request.status_code,
                    request.content.decode())

        if 'errors' in content:
            raise CoinbaseAPIException(
                    ', '.join(content['errors']),
                    request.status_code,
                    request.content.decode())

        return content
