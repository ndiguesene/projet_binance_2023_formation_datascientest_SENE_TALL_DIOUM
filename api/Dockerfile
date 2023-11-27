FROM python:3.9

LABEL maintainer="Orange DE OPA Crypto"

WORKDIR /api

ADD requirements.txt .

RUN pip3 install -r requirements.txt && rm -rf /root/.cache

COPY . .

EXPOSE 8000

# Command to run the API program
CMD python3 api.py