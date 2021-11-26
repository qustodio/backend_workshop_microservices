import os

import grpc
from apiflask import APIBlueprint, output, doc
from flask import current_app

from common.pb2 import language_pb2_grpc, language_pb2
from serializers import LanguageSchema
from views.helpers import GRPCException, returns_json

bp = APIBlueprint('language', __name__, url_prefix='/catalog/languages')

CATALOG_HOST = os.getenv("CATALOG_HOST", "localhost")
CATALOG_PORT = os.getenv("CATALOG_PORT", "50051")

GRPC_CHANNEL = grpc.insecure_channel(f"{CATALOG_HOST}:{CATALOG_PORT}")
GRPC_STUB = language_pb2_grpc.LanguageControllerStub(GRPC_CHANNEL)

languages_schema = LanguageSchema(many=True)


@bp.get('')
@doc("Get languages list")
@output(LanguageSchema(many=True))
@returns_json
def get_list():
    try:
        response = GRPC_STUB.List(language_pb2.LanguageListRequest())
    except grpc.RpcError as rpc_error:
        current_app.logger.error(rpc_error.details())
        raise GRPCException(rpc_error)
    return languages_schema.dumps(response)
