FROM debian:bullseye-slim

RUN apt update && apt upgrade -y && apt install -y python3 python3-pip curl && rm -rf /var/cache/apt/*

WORKDIR /app
COPY reverse_proxy.py /app/

RUN pip3 install -U pip wheel
RUN pip3 install Flask

CMD python3 reverse_proxy.py
