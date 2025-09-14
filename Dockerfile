FROM python:3.13

WORKDIR /app/

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --requirement requirements.txt

COPY . .
