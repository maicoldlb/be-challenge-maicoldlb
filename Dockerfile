FROM python:3.7-slim-buster

ENV TZ=America/Chicago
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY ./requirements.txt /opt/app/requirements.txt
RUN pip install -qr /opt/app/requirements.txt

COPY ./src /opt/app/src
WORKDIR /opt/app/src

CMD  gunicorn -w 5 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:3000 app:app

LABEL maintainer="maicoldemetrio@gmail.com"