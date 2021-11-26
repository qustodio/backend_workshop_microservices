import os
from uuid import UUID

import grpc
from apiflask import APIBlueprint, input, output, doc
from flask import current_app
from flask_jwt import jwt_required

from common.pb2 import book_instance_pb2, book_instance_pb2_grpc
from serializers import LoanSchema, RenewLoanSchema
from views.helpers import GRPCException, returns_json

bp = APIBlueprint('loan', __name__, url_prefix='/catalog/loans')

CATALOG_HOST = os.getenv("CATALOG_HOST", "localhost")
CATALOG_PORT = os.getenv("CATALOG_PORT", "50051")

GRPC_CHANNEL = grpc.insecure_channel(f"{CATALOG_HOST}:{CATALOG_PORT}")
GRPC_STUB = book_instance_pb2_grpc.BookInstanceControllerStub(GRPC_CHANNEL)

loan_schema = LoanSchema()
loans_schema = LoanSchema(many=True)
renew_loan_schema = RenewLoanSchema()


@bp.post('')
@doc("Create a loan")
@input(LoanSchema)
@output(LoanSchema)
@jwt_required()
def create(data: dict):
    try:
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
    return response


@bp.put('/<uuid:loan_uuid>/renew')
@doc("Renew a book on loan")
@input(RenewLoanSchema)
@output(LoanSchema)
@jwt_required()
def update(loan_uuid: UUID, data: dict):
    try:
        response = GRPC_STUB.Renew(book_instance_pb2.BookInstanceRenewal(
            id=loan_uuid.hex,
            due_back=data.get('due_back'),
        ))
    except grpc.RpcError as rpc_error:
        current_app.logger.error(rpc_error.details())
        raise GRPCException(rpc_error)

    return response


@bp.get('/my')
@doc("Get my loans")
@input(LoanSchema(partial=True))
@output(LoanSchema(many=True))
@returns_json
@jwt_required()
def get(data: dict):
    try:
        response = GRPC_STUB.MyList(book_instance_pb2.MyBookInstanceListRequest(
            borrower=data.get('borrower')
        ))
    except grpc.RpcError as rpc_error:
        current_app.logger.error(rpc_error.details())
        raise GRPCException(rpc_error)
    return loans_schema.dumps(response)


@bp.get('')
@doc("Get loans list")
@output(LoanSchema(many=True))
@returns_json
@jwt_required()
def get_list():
    try:
        response = GRPC_STUB.List(book_instance_pb2.BookInstanceListRequest())
    except grpc.RpcError as rpc_error:
        current_app.logger.error(rpc_error.details())
        raise GRPCException(rpc_error)
    return loans_schema.dumps(response)
