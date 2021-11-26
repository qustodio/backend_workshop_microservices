from common.pb2 import recommendations_pb2_grpc
from recommendations.services import RecommendationService


urlpatterns = []


def grpc_handlers(server):
    recommendations_pb2_grpc.add_RecommendationsControllerServicer_to_server(RecommendationService.as_servicer(), server)