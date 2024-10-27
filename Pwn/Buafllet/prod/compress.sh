#!/bin/sh

cd exploit
# aarch64-linux-gnu-gcc -o exploit -static exploit.c -D_GNU_SOURCE
# cp ./exploit ../initramfs
cd ../initramfs
find . -print0 \
| cpio --null -ov --format=newc \
| gzip -9 > initramfs.cpio.gz
mv ./initramfs.cpio.gz ../
cd ..