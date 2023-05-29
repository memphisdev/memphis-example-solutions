FROM docker.io/mongo:latest

WORKDIR /
RUN mkdir /mongodb-conf
COPY keyFile /mongodb-conf/
RUN chown mongodb /mongodb-conf/keyFile
RUN chmod 600 /mongodb-conf/keyFile

CMD mongod --replSet rs0 --keyFile /mongodb-conf/keyFile --bind_ip_all
