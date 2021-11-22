FROM python:3.8

COPY catalog/requirements.txt /
RUN pip install -r requirements.txt

COPY recomendator /opt/recomendator
COPY common /opt/recomendator/common
WORKDIR /opt/recomendator

EXPOSE 16000
CMD [ "python", "manage.py", "runserver", "0.0.0.0:16000" ]
