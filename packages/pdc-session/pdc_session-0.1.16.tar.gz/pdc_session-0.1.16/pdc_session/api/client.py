import time
import json

from ecceran import encrypt
from requests.models import Response
from requests.sessions import Session

from ..session_config import SessionConfig
from pdc_session.helpers.singleton import Singleton


class Client(SessionConfig, metaclass=Singleton):

    session: Session

    def __init__(self):
        self.session = Session()
        
        data = json.dumps({
            'time': int(time.time()),
            'botname': self.botname
        })
        api_data = encrypt(self.api_key, bytes(data, 'utf-8'))
        self.session.headers.update({
            'x-api-data': api_data
        })


    def get(self, path: str, params={}) -> Response:
        uri = f'{self.api_uri}/{path}'
        return self.session.get(uri, params=params)
    
    def post(self, path: str, data={}) -> Response:
        uri = f'{self.api_uri}/{path}'
        return self.session.post(uri, json=data)
    
    def put(self, path: str, data={}) -> Response:
        uri = f'{self.api_uri}/{path}'
        return self.session.put(uri, json=data)