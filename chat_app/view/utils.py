
from flask import redirect, session

def requires_user_session(funct):
    def wrapper_method(*args, **kwargs):
        if 'user_id' not in session:
            return redirect("/")
        return funct(*args, **kwargs)
    return wrapper_method