import os

import grpc
from apiflask import APIBlueprint, input, output, doc
from flask import request, current_app
from google.protobuf.json_format import MessageToJson

from common.pb2 import account_pb2_grpc, account_pb2
from serializers import AuthorSchema
from views.helpers import GRPCException, returns_json

bp = APIBlueprint('user', __name__, url_prefix='/user')

ACCOUNTS_HOST = os.getenv("ACCOUNTS_HOST", "accounts")
ACCOUNTS_PORT = os.getenv("ACCOUNTS_PORT", "50051")

GRPC_CHANNEL = grpc.insecure_channel(f"{ACCOUNTS_HOST}:{ACCOUNTS_PORT}")
GRPC_STUB = account_pb2_grpc.UserControllerStub(GRPC_CHANNEL)


@bp.post('')
@doc("Create an author")
@input(AuthorSchema)
@output(AuthorSchema)
def post(data: dict):
    try:
        response = GRPC_STUB.Create(
            account_pb2.User(
                username=data.get('username'),
                password=data.get('password')
            )
        )
    except grpc.RpcError as rpc_error:
        current_app.logger.error(rpc_error.details())
        raise GRPCException(rpc_error)

    return response


@bp.get('')
def get_list():
    try:
        response = GRPC_STUB.List(account_pb2.UserListRequest())
    except grpc.RpcError as rpc_error:
        current_app.logger.error(rpc_error.details())
        raise GRPCException(rpc_error)
    print(f'Going to: {ACCOUNTS_HOST}:{ACCOUNTS_PORT}', flush=True)
    print([_ for _ in response], flush=True)
    return [_ for _ in response]


@bp.get('/<int:user_id>')
@doc("Get an author")
@output(AuthorSchema)
def get(user_id: int):
    print(f'Going to: {ACCOUNTS_HOST}:{ACCOUNTS_PORT}', flush=True)
    try:
        response = GRPC_STUB.Retrieve(account_pb2.User(id=user_id))
    except grpc.RpcError as rpc_error:
        current_app.logger.error(rpc_error.details())
        raise GRPCException(rpc_error)
    return response