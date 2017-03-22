FROM python:3.4
ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get install -y python-dev python3-dev libldap2-dev libsasl2-dev libssl-dev

ENV APP_USER user
ENV APP_ROOT /code

RUN groupadd -r ${APP_USER} && useradd -r -m --home-dir ${APP_ROOT} -s  /usr/sbin/nologin -g ${APP_USER} ${APP_USER}
WORKDIR ${APP_ROOT}

RUN mkdir /config
ADD requirements/common.txt /config/
RUN pip install -r ../config/common.txt

USER ${APP_USER}
ADD . ${APP_ROOT}