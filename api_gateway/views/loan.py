import os
from uuid import UUID
import json

import grpc
from flask import Blueprint, request, current_app
from google.protobuf.json_format import MessageToJson

from common.pb2 import book_instance_pb2, book_instance_pb2_grpc
from serializers import LoanSchema, RenewLoanSchema
from views.helpers import GRPCException, returns_json

bp = Blueprint('loan', __name__, url_prefix='/catalogs/loans')

CATALOG_HOST = os.getenv("CATALOG_HOST", "localhost")
CATALOG_PORT = os.getenv("CATALOG_PORT", "50051")

GRPC_CHANNEL = grpc.insecure_channel(f"{CATALOG_HOST}:{CATALOG_PORT}")
GRPC_STUB = book_instance_pb2_grpc.BookInstanceControllerStub(GRPC_CHANNEL)

loan_schema = LoanSchema()
loans_schema = LoanSchema(many=True)
renew_loan_schema = RenewLoanSchema()


@bp.post('')
def create():
    request_data = request.get_json()
    data = loan_schema.load(request_data)
    try:
        current_app.logger.warning(data.get('borrower'))
        response = GRPC_STUB.Create(book_instance_pb2.BookInstance(
            id=data.get('id'),
            book=data.get('book'),
            borrower=data.get('borrower'),
            due_back=data.get('due_back'),
            imprint=data.get('imprint'),
            status=data.get('status')
        ))
    except grpc.RpcError as rpc_error:
        current_app.logger.error(rpc_error.details())
        raise GRPCException(rpc_error)
    current_app.logger.warning(response)
    return loan_schema.dump(response)


@bp.put('/<uuid:loan_uuid>/renew')
def update(loan_uuid: UUID):
    request_data = request.get_json()
    data = renew_loan_schema.load(request_data)
    try:
        response = GRPC_STUB.Renew(book_instance_pb2.BookInstanceRenewal(
            id=loan_uuid.hex,
            due_back=data.get('due_back'),
        ))
    except grpc.RpcError as rpc_error:
        current_app.logger.error(rpc_error.details())
        raise GRPCException(rpc_error)

    return renew_loan_schema.dump(response)


@bp.get('/my')
@returns_json
def get():
    request_data = request.get_json()
    data = loan_schema.load(request_data, partial=True)
    try:
        response = GRPC_STUB.MyList(book_instance_pb2.MyBookInstanceListRequest(
            borrower=data.get('borrower')
        ))
    except grpc.RpcError as rpc_error:
        current_app.logger.error(rpc_error.details())
        raise GRPCException(rpc_error)
    return loans_schema.dumps(response)


@bp.get('')
@returns_json
def get_list():
    try:
        response = GRPC_STUB.List(book_instance_pb2.BookInstanceListRequest())
    except grpc.RpcError as rpc_error:
        current_app.logger.error(rpc_error.details())
        raise GRPCException(rpc_error)
    return loans_schema.dumps(response)
