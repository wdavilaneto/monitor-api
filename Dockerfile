FROM python:3.10
USER root
ENV PYTHONUNBUFFERED 1

ADD requirements.txt /config/
RUN pip install pip --upgrade
RUN pip install -r /config/requirements.txt
RUN pip install gunicorn

ADD . /app
WORKDIR /app

RUN ./manage.py makemigrations
RUN ./manage.py migrate

EXPOSE 8080
CMD gunicorn backend.wsgi -b 0.0.0.0:8080

