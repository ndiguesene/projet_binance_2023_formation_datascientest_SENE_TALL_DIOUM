FROM ubuntu:20.04

WORKDIR /app_elastic

COPY ingest_prediction_into_elastic.py .
COPY constant.py .
COPY requirements.txt .

COPY opa_cypto_XGBoost_BTCUSDT.joblib .
COPY opa_cypto_XGBoost_ETHUSDT.joblib .
COPY opa_cypto_XGBoost_SOLUSDT.joblib .
COPY opa_cypto_XGBoost_USDCUSDT.joblib .
COPY opa_cypto_XGBoost_BNBUSDT.joblib .

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends python3-pip \
    && rm -rf /var/lib/apt/lists/*
RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["python3", "ingest_prediction_into_elastic.py"]
