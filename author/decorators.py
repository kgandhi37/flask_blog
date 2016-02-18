from functools import wraps # needed
from flask import session, request, redirect, url_for, abort

def login_required(f): # subclass f, function
    @wraps(f)
    def decorated_function(*args, **kwargs): #positional requirements
        if session.get('username') is None:
            return redirect(url_for('login', next=request.url)) # next param so that can go back to location after logging in, change login function too
        return f(*args, **kwargs)
    return decorated_function # no parentheses required now
    
def author_required(f): # subclass f, function
    @wraps(f)
    def decorated_function(*args, **kwargs): #positional requirements
        if session.get('is_author') is None:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function # no parentheses required now
    