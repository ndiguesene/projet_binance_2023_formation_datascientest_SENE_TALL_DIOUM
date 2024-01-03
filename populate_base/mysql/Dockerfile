FROM ubuntu:20.04

WORKDIR /app

COPY constant.py .
COPY app.py .
COPY requirements.txt .

# Update package lists, upgrade packages, install Python3 and pip, clean up
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["python3", "app.py"]