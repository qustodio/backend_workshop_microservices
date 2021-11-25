FROM python:3.8

COPY requirements.txt /
RUN pip install -r requirements.txt

COPY . /opt/accounts
WORKDIR /opt/accounts

EXPOSE 50051
CMD [ "python", "manage.py", "grpcrunserver", "0.0.0.0:50051", "--dev" ]

