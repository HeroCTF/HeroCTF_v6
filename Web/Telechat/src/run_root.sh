#!/bin/bash
apt update && apt install curl gcc -y
echo "HERO{3ee899a3a64fa1078b57ec3fcc6718da}" > /root/flag.txt
gcc getflag.c -o /getflag && rm getflag.c
chmod u+s /getflag
