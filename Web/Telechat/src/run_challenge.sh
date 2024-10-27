#!/bin/bash
echo "[+] Installing challenge...."

curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.0/install.sh | bash
nvm install 20

cd server; npm install; node index.js &; cd ..
cd client; npm install; electron-packager . Telechat --platform=linux --arch=x64 --out=release-builds --asar --overwrite
client_path=$(find . -name "Telechat")
BOT_REVIEW=1 $client_path
