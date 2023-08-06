import pickle
import os
from unittest.mock import patch

from . import Storage, SessionNotFound, SessionData
from ..types.client import Payload


class LocalStorage(Storage):
    dir_session: str
    
    def __init__(self, dirsession: str = '/pdc_session/') -> None:
        self.dir_session = dirsession
        if not os.path.exists(self.dir_session):
            os.makedirs(self.dir_session)
    
    def get_session(self, username: str):
        path = f'{self.dir_session}{username}.session'
        if not os.path.exists(path):
            raise SessionNotFound(path + ' not found')
        
        with open(path, 'rb') as f:
            data = pickle.load(f)
            
            session = SessionData()
            session.session_id = username
            session.session_data = data
            
            return session
    
    def update_session(self, username: str, session_id: int, session):
        payload: Payload = {
            'session': session,
            'username': username
        }
        
        self.create_session(payload, False)
    
    def create_session(self, payload: Payload, lock: bool = True):
        username = payload['username']
        data = payload['session']
        
        path = f'{self.dir_session}{username}.session'
        
        with open(path, 'w+b') as out:
            pickle.dump(data, out)
            
        session = SessionData()
        session.session_id = username
        session.session_data = data
        
        return session
    
    def lock_session(self, session_id: int):
        pass
    
    def release_session(self, session_id: int):
        pass
    
    