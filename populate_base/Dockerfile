FROM debian:latest

LABEL maintainer="Orange DE Crypto Bot OPA"

WORKDIR /app

RUN apt-get update && apt-get install python3-pip -y && pip3 install requests==2.22.0 && pip3 install pandas && pip3 install python-binance && pip3 install elasticsearch && pip3 install mysql-connector-python && rm -rf /root/.cache

COPY . .

CMD python3 app.py