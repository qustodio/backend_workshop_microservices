FROM python:3.8

COPY api_gateway/requirements.txt /
RUN pip install -r requirements.txt

COPY api_gateway /opt/api_gateway

WORKDIR /opt/api_gateway
EXPOSE 5000
ENTRYPOINT ["flask", "run", "--host=0.0.0.0", "--port=5000"]
