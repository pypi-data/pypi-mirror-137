from .client import Client
from ..types.client import Payload, Response

def find_session(username: str) -> Response:
    res = Client().get(f'/session/{username}')
    return res.json()


def create_session(payload: Payload, lock: bool) -> Response:
    data = {
        'payload': payload,
        'lock': lock
    }
    res = Client().post('/session/save', data=data)
    return res.json()


def lock_session(session_id: int) -> Response:
    res = Client().get(f'/session/lock/{session_id}')
    return res.json()


def release_session(session_id: int) -> Response:
    res = Client().get(f'/session/release/{session_id}')
    return res.json()


def update_session(session_id: int, session: bytes) -> Response:
    data = {
        'session': session
    }
    res = Client().put(f'/session/update/{session_id}', data=data)
    return res.json()