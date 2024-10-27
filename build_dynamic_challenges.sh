#!/bin/bash

PWD=$(pwd)

function build() {
    path=$1
    image_name=$2

    pushd "${PWD}/${path}"
    docker build . -t "$image_name"
    popd
}

# Image tag supports does not support uppercase letters
build "./Misc/Einstein/challenge" "einstein:latest"
build "./Misc/Moo/" "moo:latest"
build "./Misc/Cloud_Shell/challenge" "cloud_shell:latest"
build "./Misc/Free_Shell" "free_shell:latest"

build "./Web/Jinjatic/src" "jinjatic:latest"
build "./Web/ComplainIO/challenge" "complainio:latest"

build "./Pwn/Buafllet/prod" "buafllet:latest"

build "./GameHacking/v002/server" "gamehacking_v2:latest"
build "./GameHacking/v003/server" "gamehacking_v3:latest"
build "./GameHacking/v004/server" "gamehacking_v4:latest"
build "./GameHacking/v005/server" "gamehacking_v5:latest"