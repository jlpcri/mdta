FROM python:3.4-alpine
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements/common.txt /code/
RUN pip install -r requirements.txt
ADD . /code/