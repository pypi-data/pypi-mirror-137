#from ..models import Transaction
from django.utils import timezone
import datetime
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import urllib3

#local
#iotaAddressesWithoutChecksum[i] = '"' .. string.sub(v, 0, 81) .. '"'
#postContent = '{"command":"getBalances","addresses":['..strjoin(',', iotaAddressesWithoutChecksum)..
#'],"threshold":100}'
#print(postContent)
#content = connection:request("POST", iotaRequestUrl(), postContent, "application/json", headers)

#function iotaRequestUrl()
#    return "https://nodes.thetangle.org:443"

MYADDRESSES = ['FTPEQZHWPO9BPPBDKNFFLFRORFVBDSJMSEPD9LESLTXJY9WHWPHCTFJHYLWNNCOWRXZXCXZEDKTJXKCAABXLAPPRPZ']#,\
              #'JBFNSFJAWDKNXYZOVMKZDKQIPNYQYIM9RQKCBHQRHAAYYAAZFT9X9YJ9WUCEVMQXXMIDFSCGYSVALSTNZDTXUTIBNX',\
            #'9VTPZAWYEPU9SHTYBOWCWZBWDIBBKMOMDOESIXYICJVBU9SRKZMMJMLRRRFZSFSSEXQDIWIHOKZTKXKYXCRCBD9HVA',\
            #'AUJLDOLKALNCMWVKCCKIGMLXEFXKQNGZGVNMFDOL9FTKXWDJRSDCLTNZWPJGXYDBKVGNB9NTTQFFECBF9TBWKUNNMC']

class IOTAImporter(object):

    def __init__(self):
        self._apiAdress = 'https://nodes.thetangle.org:443'
        self._initRequest()
        self.addAddresses = MYADDRESSES

    def _initRequest(self):
        headers = {'Accepts': 'application/json',  'X-IOTA-API-Version': '1'}
        self.session = Session()
        self.session.headers.update(headers)

    def getTransactions(self):
        for address in self.addAddresses:
            iotaAddressWithoutCheckSum = address[0:81]
            command = {
                "command": "getBalances",
                "addresses": [iotaAddressWithoutCheckSum]
            }
            stringified = json.dumps(command)
            print(stringified)
            data = self._request(path='',**command)
            print(data)

    def test(self):
        command = {
            "command": "getBalances",
            "addresses": [
                "FTPEQZHWPO9BPPBDKNFFLFRORFVBDSJMSEPD9LESLTXJY9WHWPHCTFJHYLWNNCOWRXZXCXZEDKTJXKCAA"
            ]
        }

        command = json.dumps(command)

        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        http = urllib3.PoolManager()

        response = http.request(
            'POST',
            'https://nodes.thetangle.org:443',
            headers={
                'Content-Type': 'application/json',
                'X-IOTA-API-Version': '1'
            },
            body=command)

        results = json.loads(response.data.decode('utf-8'))
        print(json.dumps(results, indent=1, sort_keys=True))

    def addAddress(self, address):
        #{"command": "getBalances", "addresses": ['..strjoin(', ', iotaAddressesWithoutChecksum)..
        # '],"threshold":100}'
        pass


    def _request(self, path, **params):
        try:
            print(params)
            print(self.session.headers)
            params = json.dumps(params)
            response = self.session.post(self._apiAdress, params=params)
            #print(response.url)
            data = json.loads(response.text)
            if data: #data['ok'] and data["code"]==0:
                return data
            else:
                raise("Data failure:")
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)
            raise("Connection Error")

iotaTest = IOTAImporter()
iotaTest.test()