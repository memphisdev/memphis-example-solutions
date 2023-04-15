# Debezium Server Docker Image
This repository contains a Dockerfile for creating a Docker image for Debezium Server.

## Using
When launching the server, you will need to mount a (optionally read-only) directory at `/debezium-server/conf` containing the
Debezium Server configuration file `application.properties`.

## Developer Notes
I didn't see a way to just grab the latest version, so the image is currently hard-coded to 2.2.0Beta1.
