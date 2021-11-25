from django_grpc_framework import generics
from account.serializers import UserProtoSerializer
from account.models import User


class UserService(
    generics.ModelService
):
    """
    gRPC service that allows users to be retrieved or updated.
    """
    queryset = User.objects.all()
    serializer_class = UserProtoSerializer