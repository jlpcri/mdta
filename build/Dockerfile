# put daemon.json in directory: /etc/docker/
FROM python:3.4
RUN apt-get update && apt-get install -y python-dev python3-dev libldap2-dev libsasl2-dev libssl-dev
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements/common.txt /code/
RUN pip install -r common.txt
ADD . /code/:q