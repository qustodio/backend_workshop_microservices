### Important info

1. Django superuser (admin):

```json
{
  "username": "qustodio", 
  "password": "pyday123"
}
```

2. Repo with the common grpc code (pb2):
   1. [Link](https://pypi.org/project/qservices-library)
   2. Package installation: `pip install qservices-library`

### How to create all the boilerplate code for a gRPC model

1. Create the proto model:

```bash
# Needs to be in the container to have access 
# to the proper tools and paths
docker-compose run catalog python manage.py generateproto 
--model catalog.models.Book --fields=id,title,author --file book.proto
```

2. Copy&Paste the generated proto-model (from previous step) into _protobufs/catalog/book.proto_
3. Change the package name in book.proto (line 3) to catalog.
4. Create the gRPC model code (pb2):

```bash
python -m grpc_tools.protoc --proto_path=protobufs 
--python_out=common/pb2 --grpc_python_out=common/pb2 ./protobufs/catalog/book.proto
```

5. Modify the `model_pb2_grpc.py` import to match the correct package 
   p.e:

      ```python
      import recommendations_pb2 as recommendator_dot_recommendations__pb2  # FROM
      from common.pb2 import recommendations_pb2 as recommendator_dot_recommendations__pb2  # TO
      ```

6. Create the serializer class BookProtoSerializer (in catalog/catalog/serializers.py)
7. Create the service class BookService (in catalog/catalog/services.py)
8. Register the service in the grpc handler (in catalog/catalog/handlers.py)

```bash
book_pb2_grpc.add_BookControllerServicer_to_server(
    BookService.as_servicer(), 
    server
)
```

### Create DB service (docker compose local)

- Create DB service
  - Use the desired docker image for the DB
  - Include service to the network
  - Use environment variables to config container (should be in the image's documentation):
    - Username
    - Password
    - Db name
- Change django settings to use the container as the database
  - Use credentials set on the container
  - Use the db service as the database hostname

## TODO - What is missing?

In this chapter the project is almost ready, but all the GRPC model, pb2 and server-side code for the Genre model is missing.

### Steps

1. Start in the root directory
2. Create the Genre GRPC model:
   1. `docker-compose run catalog python manage.py generateproto --model catalog.models.Genre --fields=name --file genre.proto`
3. Place the `genre.proto` file in _protobufs/catalog_ directory.
4. Create the Genre GRPC pb2 code:
   1. You may need to install grpcio_tools for the next step `pip install grpcio-tools`
   2. `python -m grpc_tools.protoc --proto_path=protobufs --python_out=common/pb2 --grpc_python_out=common/pb2 ./protobufs/catalog/genre.proto`
5. Place the generated GRPC pb2 code under _common/pb2_ directory.
6. Modify the `genre_pb2_grpc.py` import to match the correct package
   p.e:

      ```python
      from catalog import genre_pb2 as catalog_dot_genre__pb2  # FROM
      from common.pb2 import genre_pb2 as catalog_dot_genre__pb2  # TO
      ```

7. Create a _GenreProtoSerializer_ class in _catalog/catalog/serializers.py_. Do not forget to:
   1. Define the class _Meta_.
   2. In meta, add the _model_, _proto_class_ and _fields_ attributes.
      1. Model = Genre
      2. Proto Class = Genre class generated in genre_pb2
      3. Fields = Genre fields to be serialized (Name)
8. Create a _GenreService_ class in _catalog/catalog/services.py_.
   1. Define the _List_ method.
   2. Query all the Genre instances
   3. Serialize all the queried instances using the _GenreProtoSerializer_.
   4. Yield every serialized genre in serializer _message_ property.
9.  Register the servicer in the GRPC handler in _catalog/catalog/handlers.py_.

#### VOILÀ! (Maybe...)

Remember that you may have to setup the application again as we added new services:

```python
make stop
make build
make run
make migrations
make migrate
make fixtures
```

### Testing

Check that `curl -X GET http://localhost:8080/api/catalog/genres` return the list of genres by _id_ and _name_.
