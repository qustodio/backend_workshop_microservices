FROM python:3.8

COPY api_gateway/requirements.txt /
RUN pip install -r requirements.txt

#RUN python -m grpc_tools.protoc -I ../protobufs --python_out=. \
#           --grpc_python_out=. ../protobufs/catalog/book.proto

WORKDIR /opt/api_gateway
EXPOSE 5000
ENTRYPOINT ["flask", "run", "--host=0.0.0.0", "--port=5000"]