# Introduction

Hi player ! Thanks for downloading and trying this challenge ! :)

# Remote Instance

For your information, the remote instance is running on Ubuntu 22.04 x86_64.

When you will have a working PoC locally, please open a ticket on the discord server. After opening it, please send your PoC code, admins will review your solution before spawning an instance (it's quite expensive).

# Instructions

In order to deploy the challenge, we can't provide a Dockerfile, as the electron application involved in this challenge needs a X server to run.

We suggest you to deploy an instance of the challenge inside a virtual machine (usually Ubuntu 22.04 as the remote instance), and also to build the client on your host. (to interact with the challenge).

## Install required package

- curl
- nodejs
- npm

## Install npm packages

```sh
$ npm install -g electron-packager
$ cd client
$ npm i
$ cd ../server/
$ npm i
```

## Build the electron application

The electron application, on the remote instance, run as a compiled binary, so do the same on the local installation !

The command to build the electron application, for a linux x64 computer is the following :

```sh
$ cd client
$ electron-packager . Telechat --platform=linux --arch=x64 --out=release --asar --overwrite
```

Please note that if you're using macos or windows, or running an 32 bits computer, the command must be changed. For example, if you're building it on windows, the command will be :

```sh
$ cd client
$ electron-packager . Telechat --platform=win32 --arch=x64 --out=release --asar --overwrite
```

If complete, you will see the binary corresponding to the electron application in the release folder.

## Setup the VM

As we suggest you, run an instance of the challenge inside a virtual machine. 

You can download the ISO from here : https://releases.ubuntu.com/jammy/ubuntu-22.04.5-desktop-amd64.iso

After the setup is done, follow those steps (run as root):

```sh
$ gcc getflag.c -o getflag
$ chmod u+s ./getflag
$ mv getflag /
$ echo "HERO{fake_flag}" > /root/flag.txt
```

For the application to work, Telechat is handling a custom protocol (deeplink) that you can find in the file "telechat.desktop".
For all URIs "telechat://" to be understand by your computer (on Ubuntu 22.04) you have to create (or move from the challenge tar archive) the file `$HOME/.local/share/applications/telechat.desktop`, containing:

```
[Desktop Entry]
Version=1.0
Name=Telechat
Comment=Telechat Application
Exec=/path/to/telechat/binary %u
Terminal=false
Type=Application
Categories=Utility;
MimeType=x-scheme-handler/telechat;
```

Here, replace `/path/to/telechat/binary` by the path where you have compiled the telechat application.

Furthermore, execute the following command : `xdg-mime default telechat.desktop x-scheme-handler/telechat` for the deeplink `telechat://` to be understand by the system.

## Run the challenge

In order to run the challenge, you can launch the Telechat application with the following environment variables :

```sh
$ cd $PATH_TO_TELECHAT # replace $PATH_TO_SOURCES by the path were you compiled the electron application
$ API_URL=http://localhost:3000 BOT_REVIEW=1 ./Telechat
```

Moreover, you have to run the nodejs server :

```sh
$ cd $PATH_TO_SOURCES # replace $PATH_TO_SOURCES by the path were you extract the challenge
$ npm install
$ PORT=3000 node index.js
```
