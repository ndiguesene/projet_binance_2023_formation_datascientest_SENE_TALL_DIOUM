FROM ubuntu:20.04

LABEL maintainer="Orange DE OPA Crypto API"

WORKDIR /server

COPY requirements.txt .
COPY app.py .
COPY constant.py .
COPY server.py .

RUN apt-get update && apt-get upgrade &&  apt-get -y install python3-pip && pip3 install -r requirements.txt && pip3 install mysql-connector-python && pip3 install python-binance && rm -rf /root/.cache

EXPOSE 9000

COPY . .
# Command to run the API program
#CMD uvicorn server:server --host 0.0.0.0
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "9000"]