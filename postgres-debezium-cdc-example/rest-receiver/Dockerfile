FROM debian:bullseye-slim

RUN apt update && apt upgrade -y && apt install -y python3 python3-pip wget && rm -rf /var/cache/apt/*

WORKDIR /app
COPY deb_receiver.py /app/

RUN pip3 install -U pip wheel
RUN pip3 install Flask

CMD python3 deb_receiver.py
