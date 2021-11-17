import os

import grpc
from flask import Blueprint, request, current_app
from google.protobuf.json_format import MessageToJson

from common.pb2 import book_instance_pb2, book_instance_pb2_grpc
from views.helpers import returns_json, GRPCException

bp = Blueprint('loan', __name__, url_prefix='/catalogs/loans')

MICROSERVICES_HOST = os.getenv("MICROSERVICES_HOST", "localhost")
MICROSERVICES_PORT = os.getenv("MICROSERVICES_PORT", "50051")

GRPC_CHANNEL = grpc.insecure_channel(f"{MICROSERVICES_HOST}:{MICROSERVICES_PORT}")
GRPC_STUB = book_instance_pb2_grpc.BookInstanceControllerStub(GRPC_CHANNEL)


@bp.post('')
@returns_json
def create():
    request_data = request.get_json()
    try:
        response = GRPC_STUB.Create(book_instance_pb2.BookInstance(
            book=request_data['book_id'],
            borrower=request_data['user_id'],
            due_back=request_data['due_back'],
            imprint=request_data['imprint'],
            status=request_data['status'] if 'status' in request_data else None
        ))
    except grpc.RpcError as rpc_error:
        current_app.logger.error(rpc_error.details())
        raise GRPCException(rpc_error)

    return MessageToJson(response)


@bp.put('/<uuid:loan_uuid>/renew')
@returns_json
def update(loan_uuid):
    request_data = request.get_json()
    try:
        response = GRPC_STUB.Renew(book_instance_pb2.BookInstanceRenewal(
            id=str(loan_uuid),
            due_back=request_data['due_back'],
        ))
    except grpc.RpcError as rpc_error:
        current_app.logger.error(rpc_error.details())
        raise GRPCException(rpc_error)

    return MessageToJson(response)


@bp.get('/my')
@returns_json
def get():
    request_data = request.get_json()
    loans = []
    try:
        response = GRPC_STUB.MyList(book_instance_pb2.MyBookInstanceListRequest(
            borrower=request_data['user_id']
        ))
        for loan in response:
            loans.append(MessageToJson(loan))
    except grpc.RpcError as rpc_error:
        current_app.logger.error(rpc_error.details())
        raise GRPCException(rpc_error)
    return loans


@bp.get('')
@returns_json
def get_list():
    loans = []
    try:
        response = GRPC_STUB.List(book_instance_pb2.BookInstanceListRequest())
        for loan in response:
            loans.append(MessageToJson(loan))
    except grpc.RpcError as rpc_error:
        current_app.logger.error(rpc_error.details())
        raise GRPCException(rpc_error)
    return loans
