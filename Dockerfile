# syntax=docker/dockerfile:1

FROM python:3.8-alpine

WORKDIR /app

COPY requirements.txt requirements.txt

RUN python3 -m pip install -r requirements.txt --no-cache-dir

COPY . .

ENV AMAZON_API_KEY=""
ENV TWILIO_ACCOUNT_SID=""
ENV TWILIO_AUTH_TOKEN=""
ENV TWILIO_PHONE_SENDER=""
ENV TWILIO_PHONE_RECEIVER=""
ENV AMAZON_PRODUCT_ID=""
ENV AMAZON_TRIGGER_HIGH_LIMIT=""
ENV AMAZON_TRIGGER_LOW_LIMIT=""
ENV CRON_INTERVAL=""

ENTRYPOINT ["sh", "/app/docker-entrypoint.sh"]