"""Generic requests class"""
import json
import requests

from pyatom_finance import config
from pyatom_finance.exceptions import AtomLoginError, StockCollectorRequesterError


class Requester:
    """Requester class for saving Atom Finance session"""

    def __init__(self):
        self.verify = True
        self.headers = {"Content-Type": "application/json"}
        self.session = requests.session()

    def create_session(self):
        """Create session saving cookies for auth"""
        payload = {
            "username": config.SETTINGS.username,
            "password": config.SETTINGS.password,
        }
        resp = self.session.request(
            "POST", config.SETTINGS.atom_signin_url, data=json.dumps(payload), headers=self.headers,
        )
        if 199 < resp.status_code < 300:
            resp = resp.json()
            if not resp["success"]:
                raise AtomLoginError(reason="Unable to login to Atom Finance", message=resp["error"])
        else:
            raise StockCollectorRequesterError(reason="Bad HTTP statuss code", message=resp.text)

    def post_request(self, query):
        """Generic post request"""
        resp = self.session.request("POST", config.SETTINGS.atom_url, data=json.dumps(query), headers=self.headers,)
        if 199 < resp.status_code < 300:
            return resp.json()
        raise StockCollectorRequesterError(reason="Bad HTTP status code", message=resp.text)
