FROM ubuntu:20.04

LABEL maintainer="Orange DE OPA Crypto KAFKA"

RUN mkdir /app_kafka

WORKDIR /app_kafka

COPY app_stream_ingest_to_kafka.py .

RUN pip install python-binance && pip install confluent_kafka && rm -rf /root/.cache

CMD python3 app_stream_ingest_to_kafka.py