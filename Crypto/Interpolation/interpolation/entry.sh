#! /bin/sh

while :
do
    socat TCP-LISTEN:${LISTEN_PORT},forever,reuseaddr,fork EXEC:'/home/sage/chall.sage'
done
