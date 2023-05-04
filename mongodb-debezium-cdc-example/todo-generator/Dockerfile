FROM debian:bullseye-slim

RUN apt update && apt upgrade -y && apt install -y python3 python3-pip && rm -rf /var/cache/apt/*

WORKDIR /app
COPY todo_generator.py /app/

RUN pip3 install -U pip wheel
RUN pip3 install pymongo

CMD python3 todo_generator.py
