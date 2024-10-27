#!/bin/bash

if ! test -f ".ctf/config"; then
    ctf init
fi

for i in $(find . -name 'challenge.y*ml' -type f 2>/dev/null)
do
    echo "--------[ INSTALL & SYNC $i ]--------"
    ctf challenge install "$PWD/$i"
	ctf challenge sync "$PWD/$i"
done

