FROM python:3.9

LABEL maintainer="Orange DE OPA Crypto"

RUN mkdir /app

WORKDIR /app

COPY constant.py .
COPY app.py .

RUN apt-get update && apt-get install python3-pip -y && pip3 install mysql-connector-python && pip3 install python-binance && rm -rf /root/.cache

CMD python3 app.py