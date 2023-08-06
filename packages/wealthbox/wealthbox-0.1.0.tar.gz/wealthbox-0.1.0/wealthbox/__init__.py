from json import JSONDecodeError
import requests

__version__ = '0.1.0'

class WealthBox(object):
    def __init__(self, token=None):
        self.token = token
        self.base_url = f"https://api.crmworkspace.com/v1/"
    
    def api_request(self, endpoint, params=None):
        url = self.base_url + endpoint
        if params is None: params = {}

        params.setdefault('per_page','5000')

        res = requests.get(url,
            params = params,
            headers={'ACCESS_TOKEN':self.token})
        
        try:
            return res.json()
        except JSONDecodeError:
            return res.text

    def get_contacts(self, filters=None):
        return self.api_request('contacts',params=filters)