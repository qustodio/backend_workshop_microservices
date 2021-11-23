from common.pb2 import recomendations_pb2_grpc
from recomendations.services import RecomendationService


urlpatterns = []


def grpc_handlers(server):
    recomendations_pb2_grpc.add_RecomendationsControllerServicer_to_server(RecomendationService.as_servicer(), server)