import werkzeug.exceptions
from flask import Flask, jsonify

from views.helpers import GRPCException

app = Flask(__name__)


@app.route("/")
def index():
    return "Hello world!"


@app.errorhandler(404)
def not_found(error):
    error_message = {
        "error": "Not found"
    }
    app.logger.error(error)
    return jsonify(error_message), 404


@app.errorhandler(GRPCException)
def gprc_exception(error):
    error = {
        "error": error.details
    }
    return jsonify(error), 400

@app.errorhandler(werkzeug.exceptions.HTTPException)
def handle_exception(error):
    app.logger.error(error)
    error = {
        "error": 'Unexpected error'
    }
    return jsonify(error), 400


from views import author
app.register_blueprint(author.bp)
from views import book
app.register_blueprint(book.bp)
