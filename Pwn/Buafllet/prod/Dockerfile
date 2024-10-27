FROM ubuntu:22.04

WORKDIR /buafllet

RUN apt-get update
RUN apt-get install qemu-system-arm vim cpio openssh-server socat -y

RUN groupadd ctf && \
    useradd -G ctf --home=/buafllet --shell /bin/bash player && \
    echo 'player:heroctf' | chpasswd && \
    mkdir /buafllet/exploit/ && \
    chown -R player:player /buafllet/exploit/

COPY Image /buafllet/
COPY ./buafllet.ko /buafllet/
COPY ./run.sh /buafllet/
COPY ./entrypoint.sh /entrypoint.sh

COPY ./initramfs.cpio.gz /buafllet/


RUN chmod 755 /buafllet/Image /buafllet/buafllet.ko /entrypoint.sh && \
    chmod 400 /buafllet/initramfs.cpio.gz


CMD ["/entrypoint.sh"]
