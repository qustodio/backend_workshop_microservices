FROM python:3.8

COPY recomendator/requirements.txt /
RUN pip install -r requirements.txt

COPY recomendator /opt/recomendator
COPY common /opt/recomendator/common
WORKDIR /opt/recomendator

EXPOSE 16000
CMD [ "/opt/recomendator/scripts/run_server_and_cqrs.sh" ]
