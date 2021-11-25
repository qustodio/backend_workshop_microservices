import os

import grpc
from flask import Blueprint, current_app

from common.pb2 import recomendations_pb2, recomendations_pb2_grpc
from serializers import RecomendationSchema
from views.helpers import returns_json, GRPCException

bp = Blueprint('recomendation', __name__, url_prefix='/recomendations')

RECOMENDATOR_HOST = os.getenv("RECOMENDATOR_HOST", "localhost")
RECOMENDATOR_PORT = os.getenv("RECOMENDATOR_PORT", "50051")

GRPC_CHANNEL = grpc.insecure_channel(f"{RECOMENDATOR_HOST}:{RECOMENDATOR_PORT}")
GRPC_STUB = recomendations_pb2_grpc.RecomendationsControllerStub(GRPC_CHANNEL)

recomendations_schema = RecomendationSchema(many=True)


@bp.get('/<int:user_id>')
@returns_json
def get_list(user_id: int):
    try:
        response = GRPC_STUB.List(recomendations_pb2.RecomendationsRequest(
            id=user_id
        ))
    except grpc.RpcError as rpc_error:
        current_app.logger.error(rpc_error.details())
        raise GRPCException(rpc_error)

    return recomendations_schema.dumps(response)
