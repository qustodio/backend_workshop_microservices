from flask import Blueprint, request

bp = Blueprint('test', __name__)


@bp.route('/create')
def create():
    request_data = request.get_json()
    return request_data
