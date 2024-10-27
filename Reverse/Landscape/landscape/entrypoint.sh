#!/bin/bash

while :
do
    su -c "export FLAG=$FLAG; exec socat TCP-LISTEN:1337,reuseaddr,fork EXEC:'/challenge/game,stderr'" - player;
done