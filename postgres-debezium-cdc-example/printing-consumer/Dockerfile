FROM python:3-slim

WORKDIR /app
COPY test_consumer.py /app/

RUN apt-get update && \
  apt-get install -y build-essential

RUN pip3 install -U pip wheel
RUN pip3 install memphis-py

CMD python3 test_consumer.py
