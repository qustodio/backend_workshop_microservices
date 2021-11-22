import os

import grpc
from flask import Blueprint, request, current_app
from google.protobuf.json_format import MessageToJson

from common.pb2 import author_pb2_grpc, author_pb2
from serializers import AuthorSchema
from views.helpers import GRPCException, returns_json

bp = Blueprint('author', __name__, url_prefix='/catalogs/authors')

CATALOG_HOST = os.getenv("CATALOG_HOST", "localhost")
CATALOG_PORT = os.getenv("CATALOG_PORT", "50051")

GRPC_CHANNEL = grpc.insecure_channel(f"{CATALOG_HOST}:{CATALOG_PORT}")
GRPC_STUB = author_pb2_grpc.AuthorControllerStub(GRPC_CHANNEL)

author_schema = AuthorSchema()
authors_schema = AuthorSchema(many=True)


@bp.post('')
def create():
    request_data = request.get_json()
    data = author_schema.load(request_data)
    try:
        current_app.logger.warning("DATE OF BIRTH %s", data.get('date_of_birth'))
        response = GRPC_STUB.Create(author_pb2.Author(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            date_of_birth=data.get('date_of_birth'),
            date_of_death=data.get('date_of_death')
        ))
    except grpc.RpcError as rpc_error:
        current_app.logger.error(rpc_error.details())
        raise GRPCException(rpc_error)

    return author_schema.dump(response)


@bp.put('/<int:author_id>')
def update(author_id: int):
    request_data = request.get_json()
    data = author_schema.load(request_data)
    try:
        response = GRPC_STUB.Update(author_pb2.Author(
            id=author_id,
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            date_of_birth=data.get('date_of_birth'),
            date_of_death=data.get('date_of_death')
        ))
    except grpc.RpcError as rpc_error:
        current_app.logger.error(rpc_error.details())
        raise GRPCException(rpc_error)

    return author_schema.dump(response)


@bp.delete('/<int:author_id>')
def delete(author_id: int):
    try:
        response = GRPC_STUB.Destroy(author_pb2.Author(
            id=author_id
        ))
    except grpc.RpcError as rpc_error:
        current_app.logger.error(rpc_error.details())
        raise GRPCException(rpc_error)

    return MessageToJson(response)


@bp.get('/<int:author_id>')
def get(author_id: int):
    try:
        response = GRPC_STUB.Retrieve(author_pb2.AuthorRetrieveRequest(
            id=author_id
        ))
    except grpc.RpcError as rpc_error:
        current_app.logger.error(rpc_error.details())
        raise GRPCException(rpc_error)

    return author_schema.dump(response)


@bp.get('')
@returns_json
def get_list():
    try:
        response = GRPC_STUB.List(author_pb2.AuthorListRequest())
    except grpc.RpcError as rpc_error:
        current_app.logger.error(rpc_error.details())
        raise GRPCException(rpc_error)

    return authors_schema.dumps(response)
