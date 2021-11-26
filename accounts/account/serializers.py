from django_grpc_framework import proto_serializers
from common.pb2 import account_pb2
from account.models import User


class UserProtoSerializer(proto_serializers.ModelProtoSerializer):
    class Meta:
        model = User
        proto_class = account_pb2.User
        fields = ['id', 'username', 'password']