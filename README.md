### How to create all the boilerplate code for a gRPC model
1. Create the proto model:
```bash
# Needs to be in the container to have access 
# to the proper tools and paths
docker-compose run python manage.py generateproto 
--model catalog.models.Book --fields=id,title,author --file book.proto
```
2. Copy&Paste the generated proto-model (from previous step) into _protobufs/catalog/book.proto_
3. Change the package name in book.proto (line 3) to catalog.
4. Create the gRPC model code:
```bash
python -m grpc_tools.protoc --proto_path=protobufs 
--python_out=common/pb2 --grpc_python_out=common/pb2 ./protobufs/catalog/book.proto
```
7. Create the serializer class BookProtoSerializer (in microservices/catalog/serializers.py)
8. Create the service class BookService (in microservices/catalog/services.py)
9. Register the service in the grpc handler (in microservices/catalog/handlers.py)
```bash
book_pb2_grpc.add_BookControllerServicer_to_server(
    BookService.as_servicer(), 
    server
)
```

