FROM debian:bullseye-slim

RUN apt update && apt upgrade -y && apt install -y openjdk-11-jre-headless wget && rm -rf /var/cache/apt/*

WORKDIR /
RUN wget https://repo1.maven.org/maven2/io/debezium/debezium-server-dist/2.2.0.Beta1/debezium-server-dist-2.2.0.Beta1.tar.gz && \
	tar -xzvf debezium-server-dist-2.2.0.Beta1.tar.gz && \
	rm -f debezium-server-dist-2.2.0.Beta1.tar.gz

WORKDIR /debezium-server
RUN mkdir data

CMD ./run.sh
