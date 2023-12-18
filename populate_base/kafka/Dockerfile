FROM python:3.9

LABEL maintainer="Orange DE OPA Crypto KAFKA"

RUN mkdir /app_kafka

WORKDIR /app_kafka

COPY app_stream_ingest_to_kafka.py .

RUN pip3 install python-binance && pip3 install confluent_kafka && rm -rf /root/.cache

CMD python3 app_stream_ingest_to_kafka.py