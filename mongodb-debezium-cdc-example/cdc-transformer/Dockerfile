FROM python:3-slim

RUN apt update && apt upgrade -y && apt install -y curl && rm -rf /var/cache/apt/*

WORKDIR /app
COPY cdc_transformer.py /app/

RUN pip3 install -U pip wheel
RUN pip3 install memphis-py

CMD python3 cdc_transformer.py
