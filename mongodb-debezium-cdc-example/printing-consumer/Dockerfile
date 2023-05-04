FROM debian:bullseye-slim

RUN apt update && apt upgrade -y && apt install -y python3 python3-pip curl && rm -rf /var/cache/apt/*

WORKDIR /app
COPY test_consumer.py /app/

RUN pip3 install -U pip wheel
RUN pip3 install memphis-py

CMD python3 test_consumer.py
