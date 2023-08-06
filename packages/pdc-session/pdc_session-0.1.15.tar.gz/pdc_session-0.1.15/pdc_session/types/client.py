from typing import Any, TypedDict
# 

class Payload(TypedDict):
    username: str
    session: str

class Response:
    error: bool
    msg: str
    data: Any