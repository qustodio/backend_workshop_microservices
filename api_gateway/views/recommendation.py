import os

import grpc
from apiflask import APIBlueprint, output, doc
from flask import current_app

from common.pb2 import book_pb2_grpc, book_pb2, recommendations_pb2, recommendations_pb2_grpc
from serializers import RecommendationSchema
from views.helpers import returns_json, GRPCException

bp = APIBlueprint('recommendation', __name__, url_prefix='/recommendations')

RECOMMENDATOR_HOST = os.getenv("RECOMMENDATOR_HOST", "localhost")
RECOMMENDATOR_PORT = os.getenv("RECOMMENDATOR_PORT", "50051")
GRPC_RECOMMENDATOR_CHANNEL = grpc.insecure_channel(f"{RECOMMENDATOR_HOST}:{RECOMMENDATOR_PORT}")
GRPC_RECOMMENDATOR_STUB = recommendations_pb2_grpc.RecommendationsControllerStub(GRPC_RECOMMENDATOR_CHANNEL)

CATALOG_HOST = os.getenv("CATALOG_HOST", "localhost")
CATALOG_PORT = os.getenv("CATALOG_PORT", "50051")
GRPC_CATALOG_CHANNEL = grpc.insecure_channel(f"{CATALOG_HOST}:{CATALOG_PORT}")
GRPC_CATALOG_STUB = book_pb2_grpc.BookControllerStub(GRPC_CATALOG_CHANNEL)

recommendations_schema = RecommendationSchema(many=True)


@bp.get('/<int:user_id>')
@doc("Get recommendations list")
@output(RecommendationSchema(many=True))
@returns_json
def get_list(user_id: int):
    try:
        book_ids = GRPC_RECOMMENDATOR_STUB.List(recommendations_pb2.RecommendationsRequest(
            id=user_id
        ))
        response = [
            GRPC_CATALOG_STUB.Retrieve(book_pb2.BookRetrieveRequest(id=book_id.id))
            for book_id in book_ids
        ]
    except grpc.RpcError as rpc_error:
        current_app.logger.error(rpc_error.details())
        raise GRPCException(rpc_error)

    return recommendations_schema.dumps(response)
