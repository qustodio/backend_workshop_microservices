import grpc

from common.pb2 import book_pb2, book_pb2_grpc

with grpc.insecure_channel('localhost:50051') as channel:
    stub = book_pb2_grpc.BookControllerStub(channel)
    print('---CREATE---')
    response = stub.Create(book_pb2.Book(
        title='The Lord of The Rings',
        isbn='0261103571',
        author=1,
        genre=[1, 5, ],
        summary='The first of the saga',
        language=40
    ))
    print(response)
