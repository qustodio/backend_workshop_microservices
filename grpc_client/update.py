import grpc

from common.pb2 import book_pb2, book_pb2_grpc

with grpc.insecure_channel('localhost:50051') as channel:
    stub = book_pb2_grpc.BookControllerStub(channel)
    print('---UPDATE---')
    response = stub.Update(book_pb2.Book(
        id=6, # To be replaced by proper ID
        title='The Lord of The Rings: The Fellowship of the Ring',
        isbn='0261103571',
        author=1,
        genre=[1, 5, ],
        summary='The first of the saga',
        language=40
    ))
    print(response)
