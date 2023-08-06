from .CoinbaseAuthentication import CoinbaseAuthentication
class CoinbaseOAuthAuthentication(CoinbaseAuthentication):
    '''
    Implements the authentication mechanism that uses an access token and a
    refresh token.
    '''

    def __init__(self, access_token, refresh_token):
        self.access_token = access_token
        self.refresh_token = refresh_token


    def get_data(self):
        return {
            'access_token': self.access_token,
            'refresh_token': self.refresh_token
        }
