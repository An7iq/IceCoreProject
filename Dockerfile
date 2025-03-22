FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN apt-get update && apt-get install -y build-essential \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

COPY volcano_detection ./volcano_detection

CMD ["python", "volcano_detection/main.py"]