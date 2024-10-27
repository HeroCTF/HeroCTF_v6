FROM ubuntu:22.04

WORKDIR /v004/

RUN apt-get update && \
    apt-get install -y socat gcc

RUN groupadd ctf && \
    useradd -G ctf --home=/v004 player

ADD ./GameServerThree /v004/GameServerThree
COPY entrypoint.sh /v004/entrypoint.sh

RUN gcc ./GameServerThree/main.c -o ./server
RUN chmod 755 ./server ./entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]