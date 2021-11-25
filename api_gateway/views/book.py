import os

import grpc
from apiflask import APIBlueprint, input, output, doc
from flask import current_app
from google.protobuf.json_format import MessageToJson

from common.pb2 import book_pb2, book_pb2_grpc
from serializers import BookSchema
from views.helpers import returns_json, GRPCException

bp = APIBlueprint('book', __name__, url_prefix='/catalogs/books')

CATALOG_HOST = os.getenv("CATALOG_HOST", "localhost")
CATALOG_PORT = os.getenv("CATALOG_PORT", "50051")

GRPC_CHANNEL = grpc.insecure_channel(f"{CATALOG_HOST}:{CATALOG_PORT}")
GRPC_STUB = book_pb2_grpc.BookControllerStub(GRPC_CHANNEL)

book_schema = BookSchema()
books_schema = BookSchema(many=True)


@bp.post('')
@doc("Create a book")
@input(BookSchema)
@output(BookSchema)
def create(data: dict):
    try:
        response = GRPC_STUB.Create(book_pb2.Book(
            title=data.get('title'),
            isbn=data.get('isbn'),
            author=data.get('author'),
            genre=data.get('genre'),
            summary=data.get('summary'),
            language=data.get('language')
        ))
    except grpc.RpcError as rpc_error:
        current_app.logger.error(rpc_error.details())
        raise GRPCException(rpc_error)

    return response


@bp.put('/<int:book_id>')
@doc("Update a book")
@input(BookSchema)
@output(BookSchema)
def update(book_id: int, data: dict):
    try:
        response = GRPC_STUB.Update(book_pb2.Book(
            id=book_id,
            title=data.get('title'),
            isbn=data.get('isbn'),
            author=data.get('author'),
            genre=data.get('genre'),
            summary=data.get('summary'),
            language=data.get('language')
        ))
    except grpc.RpcError as rpc_error:
        current_app.logger.error(rpc_error.details())
        raise GRPCException(rpc_error)

    return response


@bp.delete('/<int:book_id>')
@doc("Delete a book")
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
@doc("Get a book")
@output(BookSchema)
def get(book_id: int):
    try:
        response = GRPC_STUB.Retrieve(book_pb2.BookRetrieveRequest(
            id=book_id
        ))
    except grpc.RpcError as rpc_error:
        current_app.logger.error(rpc_error.details())
        raise GRPCException(rpc_error)

    return response


@bp.get('')
@doc("Get books list")
@output(BookSchema(many=True))
@returns_json
def get_list():
    try:
        response = GRPC_STUB.List(book_pb2.BookListRequest())
    except grpc.RpcError as rpc_error:
        current_app.logger.error(rpc_error.details())
        raise GRPCException(rpc_error)

    return books_schema.dumps(response)
