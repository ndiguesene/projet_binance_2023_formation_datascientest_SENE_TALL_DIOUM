FROM ubuntu:20.04

LABEL maintainer="Orange DE OPA Crypto API"

WORKDIR /api

COPY requirements.txt .

RUN apt-get update && apt-get -y install python3-pip && pip3 install -r requirements.txt && rm -rf /root/.cache

EXPOSE 8000

COPY . .
# Command to run the API program
CMD python3 api.py