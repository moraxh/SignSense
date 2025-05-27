FROM python:3.13-slim

WORKDIR /app/backend

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000
EXPOSE 5001

COPY . .