FROM ubuntu:20.04

LABEL maintainer="Orange DE OPA Crypto"

RUN mkdir /app

WORKDIR /app

COPY constant.py .
COPY app.py .

RUN apt-get update
RUN apt-get upgrade
RUN apt-get -y install python3-pip
RUN pip3 install mysql-connector-python
RUN pip3 install python-binance
RUN rm -rf /root/.cache

CMD python3 app.py