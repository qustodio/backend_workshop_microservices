import os
import json

import grpc
from flask import Blueprint, request, current_app
from google.protobuf.json_format import MessageToJson

from common.pb2 import book_pb2, book_pb2_grpc
from views.helpers import returns_json, GRPCException

bp = Blueprint('book', __name__, url_prefix='/catalogs/books')

CATALOG_HOST = os.getenv("CATALOG_HOST", "localhost")
CATALOG_PORT = os.getenv("CATALOG_PORT", "50051")

GRPC_CHANNEL = grpc.insecure_channel(f"{CATALOG_HOST}:{CATALOG_PORT}")
GRPC_STUB = book_pb2_grpc.BookControllerStub(GRPC_CHANNEL)


@bp.post('')
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


@bp.put('/<int:book_id>')
@returns_json
def update(book_id: int):
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


@bp.delete('/<int:book_id>')
def delete(book_id: int):
    try:
        response = GRPC_STUB.Destroy(book_pb2.Book(
            id=book_id
        ))
    except grpc.RpcError as rpc_error:
        current_app.logger.error(rpc_error.details())
        raise GRPCException(rpc_error)

    return MessageToJson(response)


@bp.get('/<int:book_id>')
@returns_json
def get(book_id: int):
    try:
        response = GRPC_STUB.Retrieve(book_pb2.BookRetrieveRequest(
            id=book_id
        ))
    except grpc.RpcError as rpc_error:
        current_app.logger.error(rpc_error.details())
        raise GRPCException(rpc_error)

    return MessageToJson(response)


@bp.get('')
@returns_json
def get_list():
    books = []
    try:
        response = GRPC_STUB.List(book_pb2.BookListRequest())
        for book in response:
            books.append(MessageToJson(book))
    except grpc.RpcError as rpc_error:
        current_app.logger.error(rpc_error.details())
        raise GRPCException(rpc_error)

    return json.dumps(books)
