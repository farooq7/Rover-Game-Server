FROM debian:jessie-slim

RUN mkdir -p /data/db
#RUN dpkg --add-architecture armhf
RUN apt-get update && apt-get install mongodb-server -y && apt-get clean

ENTRYPOINT ["/bin/bash", "-c", "mongod --bind_ip 0.0.0.0" ]

EXPOSE 27017
