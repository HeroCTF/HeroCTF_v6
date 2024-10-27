FROM ubuntu:22.04

WORKDIR /v003/

RUN apt-get update && \
    apt-get install -y socat gcc

RUN groupadd ctf && \
    useradd -G ctf --home=/v003 player

ADD ./GameServerTwo /v003/GameServerTwo
COPY entrypoint.sh /v003/entrypoint.sh

RUN gcc ./GameServerTwo/main.c -o ./server
RUN chmod 755 ./server ./entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]