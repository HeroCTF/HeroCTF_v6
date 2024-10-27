FROM python:3.12-slim

WORKDIR /challenge

RUN apt-get update \
    && apt-get -y --no-install-recommends install socat \ 
    && rm -rf /var/lib/apt/lists/*

COPY ./free_shell.py .
COPY ./entrypoint.sh .
COPY ./flag.txt .

RUN groupadd challenge \
    && useradd --no-create-home -d /challenge -g challenge challenge \
    && chown -R challenge:challenge /challenge/ \
    && chmod -R 755 /challenge/ \
    && mv flag.txt flag_$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | head -c 32).txt

ENV LISTEN_PORT 8000

EXPOSE 8000
ENTRYPOINT ["./entrypoint.sh"]