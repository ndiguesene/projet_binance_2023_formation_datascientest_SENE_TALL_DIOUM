FROM python:3.9

LABEL maintainer="Orange DE OPA Crypto API"

WORKDIR /server

COPY requirements.txt .
COPY app.py .
COPY constant.py .
COPY server.py .

RUN pip3 install -r requirements.txt && rm -rf /root/.cache

EXPOSE 9000

COPY . .
# Command to run the API program
CMD python3 server.py