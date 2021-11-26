import os

import grpc
from apiflask import APIBlueprint, output, doc
from flask import current_app

from common.pb2 import recommendations_pb2, recommendations_pb2_grpc
from serializers import RecommendationSchema
from views.helpers import returns_json, GRPCException

bp = APIBlueprint('recommendation', __name__, url_prefix='/recommendations')

RECOMENDATOR_HOST = os.getenv("RECOMENDATOR_HOST", "localhost")
RECOMENDATOR_PORT = os.getenv("RECOMENDATOR_PORT", "50051")

GRPC_CHANNEL = grpc.insecure_channel(f"{RECOMENDATOR_HOST}:{RECOMENDATOR_PORT}")
GRPC_STUB = recommendations_pb2_grpc.RecommendationsControllerStub(GRPC_CHANNEL)

recommendations_schema = RecommendationSchema(many=True)


@bp.get('/<int:user_id>')
@doc("Get recommendations list")
@output(RecommendationSchema(many=True))
@returns_json
def get_list(user_id: int):
    try:
        response = GRPC_STUB.List(recommendations_pb2.RecommendationsRequest(
            id=user_id
        ))
    except grpc.RpcError as rpc_error:
        current_app.logger.error(rpc_error.details())
        raise GRPCException(rpc_error)

    return recommendations_schema.dumps(response)
