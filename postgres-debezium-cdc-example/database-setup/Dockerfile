FROM debian:bullseye-slim

RUN apt update && apt upgrade -y && apt install -y python3 python3-pip && rm -rf /var/cache/apt/*

WORKDIR /app
COPY setup_database.py /app/

RUN pip3 install -U pip wheel
RUN pip3 install psycopg2-binary

CMD python3 setup_database.py
