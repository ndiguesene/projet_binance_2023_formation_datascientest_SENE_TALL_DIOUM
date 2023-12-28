FROM ubuntu:20.04

LABEL maintainer="Orange DE OPA Crypto API"

WORKDIR /api

COPY requirements.txt .

RUN apt-get update && apt-get upgrade && apt-get -y install python3-pip && pip3 install -r requirements.txt && pip3 install mysql-connector-python && rm -rf /root/.cache

EXPOSE 8000

COPY . .
# Command to run the API program
#CMD uvicorn api:server --host 0.0.0.0

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]