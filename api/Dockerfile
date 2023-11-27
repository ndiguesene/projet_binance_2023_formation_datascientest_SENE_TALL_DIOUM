FROM tiangolo/uvicorn-gunicorn:python3.8-slim
  
LABEL maintainer="Orange DE Infarctus 2"

WORKDIR /app

ADD requirements.txt .

RUN pip3 install -r requirements.txt \
    && rm -rf /root/.cache

COPY . .

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
