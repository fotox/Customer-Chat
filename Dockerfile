FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    python3-dev \
    python3-pip

WORKDIR /app
COPY function/requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY function .

EXPOSE 80

CMD ["python", "app.py"]
