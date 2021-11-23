FROM python:3.8

COPY recomendator/requirements.txt /
RUN pip install -r requirements.txt

COPY recomendator /opt/recomendator
COPY common /opt/recomendator/common
WORKDIR /opt/recomendator

EXPOSE 50051
CMD [ "python", "manage.py", "grpcrunserver", "0.0.0.0:50051", "--dev" ]

