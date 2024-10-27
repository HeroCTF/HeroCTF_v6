#! /bin/bash

service nginx start&
service cron start&

while :
do
    su -c "exec socat TCP-LISTEN:${LISTEN_PORT},reuseaddr,fork EXEC:'/app/server.py,stderr'" - player;
done