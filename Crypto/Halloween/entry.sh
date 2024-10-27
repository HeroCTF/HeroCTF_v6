#! /bin/sh

while :
do
    socat TCP-LISTEN:${LISTEN_PORT},forever,reuseaddr,fork EXEC:'/app/chall.py' 2>/dev/null
done
