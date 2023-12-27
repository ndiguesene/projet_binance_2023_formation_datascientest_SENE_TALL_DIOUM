FROM python:3.9

LABEL maintainer="Orange DE OPA Crypto"

RUN mkdir /app_elastic

WORKDIR /app_elastic

COPY app_data_batch_into_elastic.py .

RUN pip3 install mysql-connector-python && pip3 install python-binance && pip3 install elasticsearch && rm -rf /root/.cache

CMD python3 app_data_batch_into_elastic.py