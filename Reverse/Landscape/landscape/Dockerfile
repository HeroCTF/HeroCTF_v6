FROM debian:12-slim@sha256:f4a83aa865a2b4a064ff142aa91c713180df9fcb86ce676b5de2981029379c37

WORKDIR /challenge

RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential socat

# COPY ./game.c .
# RUN gcc -s -o game game.c
COPY ./game .
COPY ./entrypoint.sh .

RUN addgroup --system player \
    && adduser --system --home /challenge --shell /bin/bash --no-create-home --ingroup player player \
    && chown -R player:player /challenge/ \
    && chmod -R 755 /challenge/

EXPOSE 1337
CMD ["/challenge/entrypoint.sh"]