#! /bin/bash
mkdir /var/run/sshd
/usr/sbin/sshd

while :
do
    exec socat TCP-LISTEN:1337,reuseaddr,fork EXEC:'/buafllet/run.sh,stderr'
done