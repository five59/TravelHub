FROM python:3.5

ENV PYTHONUNBUFFERED 1
ENV PIP_INDEX_URL http://devpi.docker:3141/root/pypi/+simple/
ENV PIP_TRUSTED_HOST devpi.docker
ENV PATH /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

USER root
RUN mkdir /code
WORKDIR /code

RUN mkdir /root/.ptpython && touch /root/.ptpython/config.py

RUN apt-get update -y && \
    apt-get install build-essential unzip  -y

ADD ./requirements.txt /code/
RUN pip install --trusted-host devpi.docker --upgrade pip
RUN pip install --trusted-host devpi.docker -r requirements.txt
ADD . /code/
