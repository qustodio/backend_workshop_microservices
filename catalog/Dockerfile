FROM python:3.8

COPY catalog/requirements.txt /
RUN pip install -r requirements.txt

COPY catalog /opt/catalog
COPY common /opt/catalog/common
WORKDIR /opt/catalog

EXPOSE 50051
CMD [ "python", "manage.py", "grpcrunserver", "0.0.0.0:50051", "--dev" ]
