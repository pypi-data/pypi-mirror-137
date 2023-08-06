import pickle
from . import Storage, SessionNotFound, SessionData

from ..api.session import create_session, find_session, lock_session, release_session, update_session
from ..types.client import Payload
from ..types.session_exception import ReleaseZero

class CloudApiError(Exception):
    pass

class CloudStorage(Storage):
    def get_session(self, username: str) -> SessionData:
        data = find_session(username)
        
        if data['error']:
            if data['msg'] == 'no session unlock':
                raise SessionNotFound(f'{username} session not found')
        
        byte = bytes(data['data']['session_data'], 'utf-8')
        object = pickle.loads(byte)
        
        session = SessionData()
        session.session_id = data['data']['id']
        session.session_data = object
        
        return session
        
        
    
    def update_session(self, username: str, session_id: int, session):
        if not session_id:
            raise ReleaseZero(f'[{self.username}] session 0')
        
        session = pickle.dumps(session, 0).decode('utf-8')
        update = update_session(session_id, session)
        if update['error']:
            raise CloudApiError(update['msg'])
        return update
    
    def create_session(self, payload: Payload, lock: bool) -> SessionData:
        payload['session'] = pickle.dumps(payload['session'], 0).decode('utf-8')
        res = create_session(payload, lock)
        
        if res['error']:
             raise CloudApiError(res['msg'])
         
        data = res['data']['session_data']
        data = pickle.loads(bytes(data, 'utf-8'))
         
        session = SessionData()
        session.session_id = res['data']['id']
        session.session_data = data
            
        return session
    
    def lock_session(self, session_id: int):
        res = lock_session(session_id)
        if res['error']:
            raise CloudApiError(res['msg'])
        
        return res
    
    def release_session(self, session_id: int):
        res = release_session(session_id)
    
        if res['error']:
             raise CloudApiError(res['msg'])
            
        return res
    
    