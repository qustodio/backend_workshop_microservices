import werkzeug.exceptions
from flask import Response
from functools import wraps


def returns_json(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        r = f(*args, **kwargs)
        return Response(r, content_type='application/json; charset=utf-8')
    return decorated_function


class GRPCException(werkzeug.exceptions.BadRequest):
    status_code = 400

    def __init__(self, error, status_code=None):
        Exception.__init__(self)
        self.error = error
        self.details = error.details()
        if status_code is not None:
            self.status_code = status_code
