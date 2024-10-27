FROM ubuntu:22.04

WORKDIR /bankrupst/

RUN apt-get update && \
    apt-get install -y socat

RUN groupadd ctf && \
    useradd -G ctf --home=/bankrupst player

COPY ./bankrupst /bankrupst/
COPY ./entrypoint.sh /bankrupst/
COPY ./flag.txt /bankrupst/

RUN chmod 755 /bankrupst/bankrupst /bankrupst/entrypoint.sh /bankrupst/flag.txt

ENTRYPOINT ["/bankrupst/entrypoint.sh"]