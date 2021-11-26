import hmac

import marshmallow.exceptions
import werkzeug.exceptions

from common.pb2 import account_pb2
from flask import jsonify
from apiflask import APIFlask
from views.account import GRPC_STUB as account_stub
from flask_jwt import JWT

from views.helpers import GRPCException


# Authentication
def authenticate(username, password):
    user = account_stub.Retrieve(account_pb2.User(username=username))
    if user and hmac.compare_digest(user.password.encode('utf-8'), password.encode('utf-8')):
        return user


def identity(payload):
    user_id = payload['identity']
    return account_stub.Retrieve(account_pb2.User(id=user_id))


app = APIFlask(__name__, docs_path='/docs/swagger-ui')

jwt = JWT(app, authenticate, identity)


def index():
    return "Hello from Qustodio API Gateway!"


@app.errorhandler(404)
def not_found(error):
    error_message = {
        "error": "Not found"
    }
    app.logger.error(error)
    return jsonify(error_message), 404


@app.errorhandler(GRPCException)
def grpc_exception(error):
    error = {
        "error": error.details
    }
    return jsonify(error), 400


@app.errorhandler(marshmallow.exceptions.ValidationError)
def validation_error(error):
    app.logger.error(error.messages)
    error = {
        "error": error.messages
    }
    return jsonify(error), 400


@app.errorhandler(Exception)
def handle_exception(error):
    app.logger.error(error)
    if isinstance(error, werkzeug.exceptions.HTTPException) and error.code < 500:
        code = error.code
        error = {
            "error": error.description
        }
        return jsonify(error), code

    elif app.env=='development' or app.debug:
        import traceback
        tb_info = traceback.format_exc()
        app.logger.error(tb_info)
        error = {
            'error': tb_info
        }
    else:
        error = {
            'error': 'Unexpected error'
        }
    return jsonify(error), 400


from views import author

app.register_blueprint(author.bp)
from views import book

app.register_blueprint(book.bp)
from views import loan

app.register_blueprint(loan.bp)
from views import recomendation

app.register_blueprint(recomendation.bp)
from views import account

app.register_blueprint(account.bp)