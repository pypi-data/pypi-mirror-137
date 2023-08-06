from abc import ABC, abstractmethod
from typing import Union, Any

from ..types.client import Payload

class SessionNotFound(Exception):
    pass

class SessionData:
    session_id: Union[int, str]
    session_data: Any

class Storage(ABC):
    @abstractmethod
    def get_session(self, username: str) -> SessionData:
        pass
    
    @abstractmethod
    def update_session(self, username: str, session_id: int, session):
        pass
    
    @abstractmethod
    def create_session(self, payload: Payload, lock: bool) -> SessionData:
        pass
    
    @abstractmethod
    def lock_session(self, session_id: int):
        pass
    
    @abstractmethod
    def release_session(self, session_id: int):
        pass