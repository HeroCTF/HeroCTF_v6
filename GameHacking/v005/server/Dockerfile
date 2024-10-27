FROM ubuntu:22.04

WORKDIR /v005/

RUN apt-get update && \
    apt-get install -y socat gcc

RUN groupadd ctf && \
    useradd -G ctf --home=/v005 player

ADD ./GameServerFour /v005/GameServerFour
COPY entrypoint.sh /v005/entrypoint.sh

RUN gcc ./GameServerFour/main.c -o ./server
RUN chmod 755 ./server ./entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]