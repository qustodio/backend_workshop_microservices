### Description
Flask-based API gateway to handle REST<->GRPC communication between Catalog and Recommendation microservices, databases and frontend.

Marshmallow schemas are used to validate request and response data.

### Views
1. Author - connects through GRPC with the catalog microservice
2. Book - connects through GRPC with the catalog microservice
3. Loan - connects through GRPC with the catalog microservice
4. Recommendation - connects through GRPC with the recommendation microservice