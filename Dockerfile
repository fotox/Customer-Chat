FROM python:3.11-slim

WORKDIR /chat

RUN apt-get update && apt-get install -y \
    python3-dev \
    python3-pip \
    libpq-dev

WORKDIR /chat
COPY function/requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY function .

EXPOSE 8000

CMD ["python", "main.py"]
