FROM php:8.1-apache

ARG BOT_SECRET
ARG FLAG

RUN apt update && apt install -y nginx haproxy;

COPY ./apache/ /var/www/html/
COPY ./nginx/ /etc/nginx/
COPY ./haproxy/ /etc/haproxy/

RUN sed -i "s/{BOT_SECRET}/$BOT_SECRET/g" /etc/nginx/nginx.conf         && \
    sed -i "s/{FLAG}/$FLAG/g" /etc/nginx/nginx.conf                     && \
    mv /usr/local/etc/php/php.ini-production /usr/local/etc/php/php.ini && \
    rm /usr/local/etc/php/php.ini-development

CMD service nginx start && haproxy -f /etc/haproxy/haproxy.cfg & apache2-foreground