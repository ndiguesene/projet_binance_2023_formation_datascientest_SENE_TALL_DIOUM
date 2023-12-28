FROM ubuntu:20.04

LABEL maintainer="Orange DE OPA Crypto"

RUN mkdir /app_elastic

WORKDIR /app_elastic

COPY app_data_batch_into_elastic.py .

RUN apt-get update && apt-get -y install python3-pip && pip3 install mysql-connector-python && pip3 install python-binance && pip3 install elasticsearch && rm -rf /root/.cache

CMD python3 app_data_batch_into_elastic.py