FROM ubuntu:latest

RUN useradd -m elasticsearch

RUN apt-get update 
RUN apt-get install -y python3-pip
RUN apt-get install -y python3-elasticsearch

RUN apt-get install -y curl

RUN mkdir -p /scripts

WORKDIR /scripts

COPY ./for_install /opt

RUN cd /opt && tar -xzf elasticsearch-7.17.0-linux-x86_64.tar.gz
RUN chown elasticsearch:elasticsearch -R /opt/elasticsearch-7.17.0
