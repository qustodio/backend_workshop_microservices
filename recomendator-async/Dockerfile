FROM python:3.8

COPY ./requirements.txt /
RUN pip install -r requirements.txt

COPY . /opt/recomendator
WORKDIR /opt/recomendator

EXPOSE 80
CMD [ "/opt/recomendator/scripts/run_server_and_cqrs.sh" ]
