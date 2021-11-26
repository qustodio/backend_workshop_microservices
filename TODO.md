## What is missing?
In this chapter the splitting-the-monolith is almost ready, but all the GRPC model, pb2 and server-side code for the Genre model is missing.

### Steps
1. Start in the root directory
2. Create the Genre GRPC model:
   1. `docker-compose run catalog python manage.py generateproto --model catalog.models.Genre --fields=id,title,author --file genre.proto`
3. Place the `genre.proto` file in _protobufs/catalog_ directory.
4. Create the Genre GRPC pb2 code:
   1. `python -m grpc_tools.protoc --proto_path=protobufs --python_out=common/pb2 --grpc_python_out=common/pb2 ./protobufs/catalog/genre.proto`
5. Place the generated GRPC pb2 code under _common/pb2_ directory.
6. Create a _GenreProtoSerializer_ class in _catalog/catalog/serializers.py_. Do not forget to:
   1. Define the class _Meta_.
   2. In meta, add the _model_, _proto_class_ and _fields_ attributes.
   3. Fields attribute may contain the only to fields that represent the Genre model (id, name).
7. Create a _LanguageService_ class in _catalog/catalog/services.py_.
   1. Define the _List_ method.
   2. Query all the Genre instances
   3. Serialize all the queried instances using the _GenreProtoSerializer_.
   4. Yield every serialized genre in serializer _message_ property.
8. Register the servicer in the GRPC handler in _catalog/catalog/services.py_.

#### VOILÀ!

### Testing
Check that `curl -X GET http://localhost:8080/api/catalog/genres` return the list of genres by _id_ and _name_.