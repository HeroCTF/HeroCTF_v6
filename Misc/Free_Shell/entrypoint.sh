#!/bin/bash

echo "Listening on port ${LISTEN_PORT}"

while :
do
    su -c "exec socat TCP-LISTEN:${LISTEN_PORT},reuseaddr,fork EXEC:'/challenge/free_shell.py,stderr'" - challenge;
done