#!/bin/sh
ssh-keygen -A
rc-status
touch /run/openrc/softlevel
/etc/init.d/sshd start
su - gaoler -c 'python3 /server/receiver.py'