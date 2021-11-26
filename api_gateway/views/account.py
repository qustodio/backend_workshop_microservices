import json
import os

import grpc
from apiflask import APIBlueprint, input, output, doc
from flask import request, current_app
from flask_jwt import jwt_required, current_identity
from google.protobuf.json_format import MessageToJson

from common.pb2 import account_pb2_grpc, account_pb2
from serializers import AuthorSchema
from views.helpers import GRPCException, returns_json
from serializers import UserSchema

bp = APIBlueprint('users', __name__, url_prefix='/user')

ACCOUNTS_HOST = os.getenv("ACCOUNTS_HOST", "accounts")
ACCOUNTS_PORT = os.getenv("ACCOUNTS_PORT", "50051")

GRPC_CHANNEL = grpc.insecure_channel(f"{ACCOUNTS_HOST}:{ACCOUNTS_PORT}")
GRPC_STUB = account_pb2_grpc.UserControllerStub(GRPC_CHANNEL)


@bp.post('')
@doc('Create a user')
@output(UserSchema)
@jwt_required()
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


@bp.get('/me')
@doc('Retrieves back the data related with the logged user')
@jwt_required()
def get():
    try:
        response = GRPC_STUB.Retrieve(account_pb2.User(id=user_id))
    except grpc.RpcError as rpc_error:
        current_app.logger.error(rpc_error.details())
        raise GRPCException(rpc_error)
    del response['password']
    return response
