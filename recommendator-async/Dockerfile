FROM python:3.8

COPY ./requirements.txt /
RUN pip install -r requirements.txt

COPY . /opt/recommendator
WORKDIR /opt/recommendator

EXPOSE 50051
CMD [ "python", "manage.py",  "startserver" ]
