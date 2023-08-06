import json
import urllib.request

class Currency(object):
    """
    This is a generic class for representing a currency,
    """

    @property
    def symbol(self):
        """
        The symbol name of the coin which is a short form of the coin name.
        Returns:
            The symbol name of the coin
        """
        return self.__symbol

    @property
    def name(self):
        """
        The name of the coin.
        Returns:
            The full name of the coin
        """
        return self.__name

    def __init__(self, name, symbol, **kwargs):
        super().__init__()

        self.__name = name
        self.__symbol = symbol

    def __str__(self):
        return self.__symbol


class CryptoCurrency(Currency):
    """
    This is a special type of currency. In order to initialize a CrpytoCurrency, use can use the `CryptoList` which will
    query coinmarketcap in order to retrieve a list of all available cryptocurrency coins/tokens.
    """

    def __init__(self, id, **kwargs):
        super().__init__(**kwargs)

        self.__id = id

    @property
    def id(self):
        """
        The id of the coin given by the coinmarketcap API.
        Returns:
            The id of the coin
        """
        return self.__id


class CryptoList(list):
    """
    This class is a list of all available crypto coins with each coin represented by its symbol name.
    On initialization, the list of crypto coins will be queried using the APIv2 of coinmarketcap.
    """

    _COINTMARKETCAP_QUERY_LISTING = 'https://api.coinmarketcap.com/v2/listings/'

    def __query_coinmarketcap(self):

        with urllib.request.urlopen(self._COINTMARKETCAP_QUERY_LISTING) as response:
            data = json.loads(response.read().decode())

            if data:
                return data['data']

    def __init__(self):

        super().__init__()

        self._coin_map = {}

        for entry in self.__query_coinmarketcap():
            c = CryptoCurrency(**entry)

            self.append(c)

            self._coin_map[c.symbol] = c

    def find_symbol(self, symbol):

        if symbol not in self._coin_map:

            if symbol == "IOTA":
                return self._coin_map["MIOTA"]

        else:
            return self._coin_map[symbol]