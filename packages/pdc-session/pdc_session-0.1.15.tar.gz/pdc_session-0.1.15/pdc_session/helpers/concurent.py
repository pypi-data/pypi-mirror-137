from functools import wraps

from ..session_persist import SessionPersist

def session_call(user: SessionPersist):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with user:
                return func(*args, **kwargs)
        
        return wrapper
    
    return decorator