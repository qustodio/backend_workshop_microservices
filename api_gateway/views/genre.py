import os

import grpc
from apiflask import APIBlueprint, output, doc
from flask import current_app

from common.pb2 import genre_pb2_grpc, genre_pb2
from serializers import GenreSchema
from views.helpers import GRPCException, returns_json

bp = APIBlueprint('genre', __name__, url_prefix='/catalogs/genres')

CATALOG_HOST = os.getenv("CATALOG_HOST", "localhost")
CATALOG_PORT = os.getenv("CATALOG_PORT", "50051")

GRPC_CHANNEL = grpc.insecure_channel(f"{CATALOG_HOST}:{CATALOG_PORT}")
GRPC_STUB = genre_pb2_grpc.GenreControllerStub(GRPC_CHANNEL)

genres_schema = GenreSchema(many=True)


@bp.get('')
@doc("Get languages list")
@output(GenreSchema(many=True))
@returns_json
def get_list():
    try:
        response = GRPC_STUB.List(genre_pb2.GenreListRequest())
    except grpc.RpcError as rpc_error:
        current_app.logger.error(rpc_error.details())
        raise GRPCException(rpc_error)
    return genres_schema.dumps(response)
