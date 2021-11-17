import os

import grpc
from flask import Blueprint, request, current_app
from google.protobuf.json_format import MessageToJson

from common.pb2 import author_pb2_grpc, author_pb2
from views.helpers import returns_json, GRPCException

bp = Blueprint('author', __name__, url_prefix='/catalogs/authors')

MICROSERVICES_HOST = os.getenv("MICROSERVICES_HOST", "localhost")
MICROSERVICES_PORT = os.getenv("MICROSERVICES_PORT", "50051")

GRPC_CHANNEL = grpc.insecure_channel(f"{MICROSERVICES_HOST}:{MICROSERVICES_PORT}")
GRPC_STUB = author_pb2_grpc.AuthorControllerStub(GRPC_CHANNEL)


@bp.post('')
@returns_json
def create():
    request_data = request.get_json()
    try:
        response = GRPC_STUB.Create(author_pb2.Author(
            first_name=request_data['first_name'],
            last_name=request_data['last_name'],
            date_of_birth=request_data['date_of_birth'],
            date_of_death=request_data['date_of_death'],
        ))
    except grpc.RpcError as rpc_error:
        current_app.logger.error(rpc_error.details())
        raise GRPCException(rpc_error)

    return MessageToJson(response)


@bp.put('/<int:author_id>')
@returns_json
def update(author_id):
    request_data = request.get_json()
    try:
        response = GRPC_STUB.Update(author_pb2.Author(
            id=author_id,
            first_name=request_data['first_name'],
            last_name=request_data['last_name'],
            date_of_birth=request_data['date_of_birth'],
            date_of_death=request_data['date_of_death'],
        ))
    except grpc.RpcError as rpc_error:
        current_app.logger.error(rpc_error.details())
        raise GRPCException(rpc_error)

    return MessageToJson(response)


@bp.delete('/<int:author_id>')
def delete(author_id):
    try:
        response = GRPC_STUB.Destroy(author_pb2.Author(
            id=author_id
        ))
    except grpc.RpcError as rpc_error:
        current_app.logger.error(rpc_error.details())
        raise GRPCException(rpc_error)

    return MessageToJson(response)


@bp.get('/<int:author_id>')
@returns_json
def get(author_id):
    try:
        response = GRPC_STUB.Retrieve(author_pb2.AuthorRetrieveRequest(
            id=author_id
        ))
    except grpc.RpcError as rpc_error:
        current_app.logger.error(rpc_error.details())
        raise GRPCException(rpc_error)

    return MessageToJson(response)


@bp.get('')
@returns_json
def get_list():
    authors = []
    try:
        response = GRPC_STUB.List(author_pb2.AuthorListRequest())
        for author in response:
            authors.append(MessageToJson(author))
    except grpc.RpcError as rpc_error:
        current_app.logger.error(rpc_error.details())
        raise GRPCException(rpc_error)

    return authors
