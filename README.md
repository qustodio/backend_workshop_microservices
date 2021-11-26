# Making services asynchronous with CQRS

### Important info

1. Django superuser (admin):

```json
{
  "username": "qustodio", 
  "password": "pyday123"
}
```

### CQRS

(Command and Query Responsability Segregation)
Uses a MQTT service to comunicate commands to different services that are 'subscribed' to them;
    p.e:
        - A new user is created
        - A command telling that the user is created
        - A service receives the command with the created user and process the data

The MQTT service that we'll be using is [RabbitMQ](https://hub.docker.com/_/rabbitmq).
[django-cqrs](https://github.com/cloudblue/django-cqrs) will be used in order to sync django models.

### How to setup django-cqrs models to sync

1. Find the producer `models.Model` you want to sync.
   1. In this branch, **`catalog.models.Book`** could be your producer
2. Find the replica `models.Model` to sync with the producer.
   1. In this branch, **`recomendator-async.models.Book`** should be your replica
   2. The replica model does'nt have to be exactly the same as the producer.
   3. Note that the replica model will receive the producer model events.
3. Implement Mixins
   1. The producer should implement `dj_cqrs.mixins.MasterMixin`
   2. The replica should implement  `dj_cqrs.mixins.ReplicaMixin`
4. Setup model `CQRS_ID` class variable to identify the events in both models
   1. `CQRS_ID` is an string that identifies the topic inside of the MQTT service
   2. `CQRS_ID` should be the same between both models
   3. `CQRS_FIELDS` identifies the model fields to be sent throught MQTT. It have to contain
      the model `pk`
   4. **catalog.models.Book** should also implement `CQRS_FIELDS` to avoid sending the image or genre fields, you may have to also add `id` to the array as it is the `PK`

      ```python
      CQRS_ID = 'book'
      CQRS_FIELDS = (
         'id',
         'title',
         'author',
         'summary',
         'isbn',
         'language'
      )
      ```

5. Refresh the deploy
   1. `make stop`
   2. `make build`
   3. `make run`
   4. `make migrations`
   5. `make migrate`
   6. `make fixtures`
6. Enjoy (Hopefully)

### What are you doing?

This process will create a new queue and exchange in RabbitMQ
where the events will be published using the topics specified in `CQRS_ID`

When ever a new `catalog.model.User` is created/updated/modified/deleted a new event with this data
is published in the MQTT with `CQRS_ID` other models in other services with the same `CQRS_ID` will then consume
the events and process the received data.

### Remember to setup the app

```bash
make stop
make build
make run
make migrations
make migrate
make fixtures
```
