FROM python:3.9

LABEL maintainer="Orange DE OPA Crypto API"

WORKDIR /api

COPY requirements.txt .

RUN pip3 install -r requirements.txt && rm -rf /root/.cache

EXPOSE 8000

COPY . .
# Command to run the API program
CMD python3 api.py