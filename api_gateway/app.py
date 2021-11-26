import marshmallow.exceptions
import werkzeug.exceptions
from flask import jsonify
from apiflask import APIFlask

from views.helpers import GRPCException

app = APIFlask(__name__, docs_path='/docs/swagger-ui')


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

    elif app.env == 'development' or app.debug:
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
from views import genre
app.register_blueprint(genre.bp)
from views import language
app.register_blueprint(language.bp)
from views import loan
app.register_blueprint(loan.bp)
from views import recommendation
app.register_blueprint(recommendation.bp)
