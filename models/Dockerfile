FROM ubuntu:20.04

WORKDIR /model_api

# Copy requirements first to leverage Docker's layer caching
COPY requirements.txt .
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends python3-pip
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY app_old.py .
COPY constant.py .
COPY server.py .

# Cleanup APT cache
RUN apt-get clean \
    && apt-get autoclean \
    && rm -rf /var/lib/apt/lists/* \
    && rm -f /var/cache/apt/archives/*.deb /var/cache/apt/archives/partial/*.deb /var/cache/apt/*.bin

EXPOSE 9000

# Command to run the FastAPI server
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "9000"]
