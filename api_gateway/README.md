### Description
[APIFlask](https://apiflask.com)-based API gateway to handle REST<->GRPC communication between Catalog and Recommendation microservices, databases and frontend.

[Marshmallow](https://marshmallow.readthedocs.io/en/stable/) schemas are used to validate request and response data.

[Swagger-ui](https://swagger.io/docs/) is used to expose the endpoints documentation.

### Views
1. Author - connects through GRPC with the catalog microservice
2. Book - connects through GRPC with the catalog microservice
3. Loan - connects through GRPC with the catalog microservice
4. Recommendation - connects through GRPC with the recommendation microservice
5. Language - connects through GRPC with the catalog microservice
5. Genre - connects through GRPC with the catalog microservice

### Swagger-UI
Visit _http://localhost/docs/swagger-ui_