import pickle
from typing import Union

from requests import Session

from .session_config import SessionConfig
from .types.client import Payload
from .helpers.logger import create_logger

from .storage import Storage, SessionNotFound
from .storage.local_storage import LocalStorage
from .storage.cloud_storage import CloudStorage

logger = create_logger(__name__)

( lOCAL_STORAGE, PDC_CLOUD ) = ('local_storage', 'pdc_cloud')

_config_session = {
    'storage': LocalStorage()
}

def change_storage(storage: Union[str, Storage]):
    if isinstance(storage, str):
        if storage == lOCAL_STORAGE:
            _config_session['storage'] = LocalStorage()
        elif storage == PDC_CLOUD:
            _config_session['storage'] = CloudStorage()
        else:
            raise Exception('Invalid storage type string')
        
    _config_session['storage'] = storage


class SessionPersist(SessionConfig):
    
    username: str
    session: Session
    session_id: int
    session_valid: bool
    
    picks: list = ['username', 'session']
    
    @property
    def session_storage(self):
        return _config_session['storage']

    def __enter__(self):
        self._acquire()
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        self._release()


    def get_session(self):

        logger.debug('get session')
        try:
            data = self.session_storage.get_session(self.username)
        except SessionNotFound as e:
            self.session_valid = False
            logger.error(e)
            self.all_locked()
            
            return

        self.__dict__.update(data.session_data)
        self.session_id = data.session_id
        self.session_valid = True


    def update_session(self) -> bool:

        logger.debug('update session')

        data = {}
        for key, value in self.__dict__.items():
            if key in self.picks:
                data[key] = value

        session_id = self.session_id
        self.session_storage.update_session(self.username, session_id, data)
        
        return True


    def lock_session(self):
        
        logger.debug('lock session')
        self.session_storage.lock_session(self.session_id)
        return True


    def release_session(self):

        logger.debug('release session')
        self.session_storage.release_session(self.session_id)
        
        return True


    def create(self, lock=True):

        logger.debug('create session')
        data = {}
        for key, value in self.__dict__.items():
            if key in self.picks:
                data[key] = value

        payload: Payload = {
            "username": self.username,
            "session": data
        }
        session = self.session_storage.create_session(payload, lock)

        if lock:
            self.session_valid = True
            self.session_id = session.session_id
            self.__dict__.update(session.session_data)


    def all_locked(self):
        pass


    def _acquire(self):
        # set default
        self.session = Session()
        self.session_id = 0
        self.session_valid = False

        # get session
        self.get_session()
        
        if self.session_valid:
            self.lock_session()


    def _release(self):
        
        if self.session_valid:
            self.update_session()
            self.release_session()



if __name__ == '__main__':
    class Auth(SessionPersist):

        def __init__(self, username):
            self.username = username

    with Auth('test') as sp:      
        print(sp.api_uri)  
        sp.create()
        print(sp.session.cookies.get_dict())