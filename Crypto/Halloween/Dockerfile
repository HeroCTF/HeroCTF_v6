FROM python:3.11-alpine

RUN apk --update add socat \
	&& adduser -D --home /app user \
	&& pip3 install gostcrypto

COPY --chown=user . /app

RUN chmod 755 /app/entry.sh /app/chall.py

WORKDIR /app

EXPOSE ${LISTEN_PORT}

ENTRYPOINT ["/app/entry.sh"]