import os

import grpc
from apiflask import APIBlueprint, output, doc
from flask import current_app

from common.pb2 import book_pb2, book_pb2_grpc, recomendations_pb2, recomendations_pb2_grpc
from serializers import RecomendationSchema
from views.helpers import returns_json, GRPCException

bp = APIBlueprint('recomendation', __name__, url_prefix='/recomendations')

RECOMENDATOR_HOST = os.getenv("RECOMENDATOR_HOST", "localhost")
RECOMENDATOR_PORT = os.getenv("RECOMENDATOR_PORT", "50051")
GRPC_RECOMENDATOR_CHANNEL = grpc.insecure_channel(f"{RECOMENDATOR_HOST}:{RECOMENDATOR_PORT}")
GRPC_RECOMENDATOR_STUB = recomendations_pb2_grpc.RecomendationsControllerStub(GRPC_RECOMENDATOR_CHANNEL)

CATALOG_HOST = os.getenv("CATALOG_HOST", "localhost")
CATALOG_PORT = os.getenv("CATALOG_PORT", "50051")
GRPC_CATALOG_CHANNEL = grpc.insecure_channel(f"{CATALOG_HOST}:{CATALOG_PORT}")
GRPC_CATALOG_STUB = book_pb2_grpc.BookControllerStub(GRPC_CATALOG_CHANNEL)

recomendations_schema = RecomendationSchema(many=True)

RECOMENDATION_CHANNEL = grpc.insecure_channel(f"{RECOMENDATOR_HOST}:{RECOMENDATOR_PORT}")
RECOMENDATION_STUB = recomendations_pb2_grpc.RecomendationsControllerStub(RECOMENDATION_CHANNEL)

RECOMENDATOR_ASYNC_HOST = os.getenv("RECOMENDATOR_ASYNC_HOST", "localhost")
RECOMENDATOR_ASYNC_PORT = os.getenv("RECOMENDATOR_ASYNC_PORT", "50051")

RECOMENDATION_ASYNC_CHANNEL = grpc.insecure_channel(f"{RECOMENDATOR_ASYNC_HOST}:{RECOMENDATOR_ASYNC_PORT}")
RECOMENDATION_ASYNC_STUB = recomendations_pb2_grpc.RecomendationsControllerStub(RECOMENDATION_ASYNC_CHANNEL)

@bp.get('/<int:user_id>')
@doc("Get recomendations list")
@output(RecomendationSchema(many=True))
@returns_json
def get_list(user_id: int):
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
        response = [
            GRPC_CATALOG_STUB.Retrieve(book_pb2.BookRetrieveRequest(id=book_id.id))
            for book_id in book_ids
        ]
    except grpc.RpcError as rpc_error:
        current_app.logger.error(rpc_error.details())
        raise GRPCException(rpc_error)

    return recomendations_schema.dumps(response)
