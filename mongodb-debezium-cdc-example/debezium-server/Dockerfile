FROM debian:bullseye-slim

RUN apt update && apt upgrade -y && apt install -y openjdk-11-jdk-headless wget git curl && rm -rf /var/cache/apt/*

WORKDIR /
RUN git clone https://github.com/debezium/debezium
WORKDIR /debezium
RUN ./mvnw clean install -DskipITs -DskipTests
WORKDIR /
RUN git clone https://github.com/debezium/debezium-server debezium-server-build
WORKDIR /debezium-server-build
RUN ./mvnw package -DskipITs -DskipTests -Passembly
RUN tar -xzvf debezium-server-dist/target/debezium-server-dist-*.tar.gz -C /
WORKDIR /debezium-server
RUN mkdir data

CMD ./run.sh
