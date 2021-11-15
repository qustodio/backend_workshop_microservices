import os

import grpc
from flask import Blueprint, request, current_app, make_response
from google.protobuf.json_format import MessageToJson

from common.pb2 import book_pb2, book_pb2_grpc
from views.helpers import returns_json, GRPCException

bp = Blueprint('book', __name__, url_prefix='/catalog/book')

MICROSERVICES_HOST = os.getenv("MICROSERVICES_HOST", "localhost")
MICROSERVICES_PORT = os.getenv("MICROSERVICES_PORT", "50051")

GRPC_CHANNEL = grpc.insecure_channel(f"{MICROSERVICES_HOST}:{MICROSERVICES_PORT}")
GRPC_STUB = book_pb2_grpc.BookControllerStub(GRPC_CHANNEL)


@bp.post('/')
@returns_json
def create():
    request_data = request.get_json()
    try:
        response = GRPC_STUB.Create(book_pb2.Book(
            title=request_data['title'],
            isbn=request_data['isbn'],
            author=request_data['author'],
            genre=request_data['genre'],
            summary=request_data['summary'],
            language=request_data['language']
        ))
    except grpc.RpcError as rpc_error:
        current_app.logger.error(rpc_error.details())
        raise GRPCException(rpc_error)

    return MessageToJson(response)


@bp.put('/<book_id:int>')
@returns_json
def update(book_id):
    request_data = request.get_json()
    try:
        response = GRPC_STUB.Update(book_pb2.Book(
            id=book_id,
            title=request_data['title'],
            isbn=request_data['isbn'],
            author=request_data['author'],
            genre=request_data['genre'],
            summary=request_data['summary'],
            language=request_data['language']
        ))
    except grpc.RpcError as rpc_error:
        current_app.logger.error(rpc_error.details())
        raise GRPCException(rpc_error)

    return MessageToJson(response)


@bp.delete('/<book_id:int>')
def delete():
    request_data = request.get_json()
    try:
        response = GRPC_STUB.Create(book_pb2.Book(
            title=request_data['title'],
            isbn=request_data['isbn'],
            author=request_data['author'],
            genre=request_data['genre'],
            summary=request_data['summary'],
            language=request_data['language']
        ))
    except grpc.RpcError as rpc_error:
        current_app.logger.error(rpc_error.details())
        raise GRPCException(rpc_error)

    return MessageToJson(response)
