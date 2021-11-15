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
    return jsonify(error_message)


@app.errorhandler(GRPCException)
def not_found(error):
    error = {
        "error": error.details
    }
    return jsonify(error)


from views import book
app.register_blueprint(book.bp)
from views import test
app.register_blueprint(test.bp)
