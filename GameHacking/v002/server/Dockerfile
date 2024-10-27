FROM ubuntu:22.04

WORKDIR /v002/

RUN apt-get update && \
    apt-get install -y socat gcc

RUN groupadd ctf && \
    useradd -G ctf --home=/v002 player

ADD ./GameServerOne /v002/GameServerOne
COPY entrypoint.sh /v002/entrypoint.sh

RUN gcc ./GameServerOne/main.c -o ./server
RUN chmod 755 ./server ./entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]