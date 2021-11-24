#!/bin/bash

python manage.py cqrs_consume -w 2 &
python manage.py runserver 0.0.0.0:80