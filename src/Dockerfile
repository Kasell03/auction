FROM python:3.12.3-slim

WORKDIR /app/src

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

ENV PYTHONPATH=/app/src

EXPOSE 8000
