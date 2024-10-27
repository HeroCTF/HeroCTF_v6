FROM alpine:3.20.3

WORKDIR /usr/app
COPY ./src/ .
COPY ./.flag.txt /.flag.txt
RUN apk add --update --no-cache nodejs npm && \
    npm install

USER guest
CMD ["/usr/bin/node", "/usr/app/app.js"]
