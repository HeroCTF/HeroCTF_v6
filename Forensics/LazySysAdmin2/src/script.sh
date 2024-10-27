#!/bin/bash

RANDOM_NUMBER=$(shuf -i 1-13 -n 1)

INSUTLS=$(curl -s https://pastebin.com/raw/59mL2V9i)
temp=$(echo "$INSUTLS" | sed -n "${RANDOM_NUMBER}p" )

echo $temp | base64 -id

touch ./test
cat > ./test <<EOF
Oui Ouib

baguette
EOF
