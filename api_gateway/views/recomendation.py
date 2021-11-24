import os
import json

import grpc
from flask import Blueprint, current_app
from google.protobuf.json_format import MessageToJson

from common.pb2 import recomendations_pb2, recomendations_pb2_grpc
from views.helpers import returns_json, GRPCException

bp = Blueprint('recomendation', __name__, url_prefix='/recomendations')

RECOMENDATOR_HOST = os.getenv("RECOMENDATOR_HOST", "localhost")
RECOMENDATOR_PORT = os.getenv("RECOMENDATOR_PORT", "50051")

RECOMENDATION_CHANNEL = grpc.insecure_channel(f"{RECOMENDATOR_HOST}:{RECOMENDATOR_PORT}")
RECOMENDATION_STUB = recomendations_pb2_grpc.RecomendationsControllerStub(RECOMENDATION_CHANNEL)

RECOMENDATOR_ASYNC_HOST = os.getenv("RECOMENDATOR_ASYNC_HOST", "localhost")
RECOMENDATOR_ASYNC_PORT = os.getenv("RECOMENDATOR_ASYNC_PORT", "50051")

RECOMENDATION_ASYNC_CHANNEL = grpc.insecure_channel(f"{RECOMENDATOR_ASYNC_HOST}:{RECOMENDATOR_ASYNC_PORT}")
RECOMENDATION_ASYNC_STUB = recomendations_pb2_grpc.RecomendationsControllerStub(RECOMENDATION_ASYNC_CHANNEL)

@bp.get('/<int:user_id>')
@returns_json
def get_list(user_id: int):
    books = []
    try:
        response = RECOMENDATION_STUB.List(recomendations_pb2.RecomendationsRequest(
            id=user_id
        ))
        for book in response:
            books.append(MessageToJson(book))
    except grpc.RpcError as rpc_error:
        current_app.logger.error(rpc_error.details())
        raise GRPCException(rpc_error)

    return json.dumps(books)

@bp.get('async/<int:user_id>')
@returns_json
def get_list_async(user_id: int):
    books = []
    try:
        response = RECOMENDATION_ASYNC_STUB.List(recomendations_pb2.RecomendationsRequest(
            id=user_id
        ))
        for book in response:
            books.append(MessageToJson(book))
    except grpc.RpcError as rpc_error:
        current_app.logger.error(rpc_error.details())
        raise GRPCException(rpc_error)

    return json.dumps(books)
