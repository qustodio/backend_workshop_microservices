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


@app.errorhandler(Exception)
def handle_exception(error):
    app.logger.error(error)
    if app.env == 'development' or app.debug:
        import traceback
        tb_info = traceback.format_exc()
        app.logger.error(tb_info)
        error = {
            'error': tb_info
        }
    else:
        error = {
            "error": 'Unexpected error'
        }
    return jsonify(error), 400


from views import author
app.register_blueprint(author.bp)
from views import book
app.register_blueprint(book.bp)
