FROM alpine:latest

# Add utilites
RUN apk add openssh busybox python3 openrc cargo sudo
# End

# Setup flag user
RUN adduser -D -s "/bin/sh" gaoler && \
    mkdir /home/gaoler/.ssh/ && \
    chown gaoler:gaoler /home/gaoler/.ssh/ && \
    chmod 700 /home/gaoler/.ssh/ && \
    echo 'gaoler:807ee708ee266428ca1039d1ac778688' | chpasswd
# End

# Setup flag
COPY ./gaoler_very_very_secret_key.txt /root/
# End


# Setup jail environment
WORKDIR /jail/
RUN mkdir bin/ tmp/ dev/ etc/ usr/ && \
    cp /bin/cat bin/cat && \
    cp /bin/ls bin/ls && \
    cp /bin/sh bin/sh && \
    cp -r /lib/ . && \
    cp -r /usr/lib/ usr/ && \
    chown gaoler:gaoler dev/ && \
    chmod 777 tmp/
# End

# Build client inside alpine
WORKDIR /build/
COPY ./client/ .
COPY ./jail.c .
COPY ./getflag.c .
RUN cargo build --release && \
    mv /build/target/release/client /jail/bin/cloud_cat && \
    gcc jail.c -o jail && \
    mv jail /bin/ && \
    chmod u+s /bin/jail && \
    gcc getflag.c -o getthatsuperflag && \
    cp getthatsuperflag / && \
    chmod u+s /getthatsuperflag

WORKDIR /
RUN rm -rf /build/
# End

# Setup some config things
RUN adduser -D -s "/bin/jail" restricted && \
    echo 'restricted:restricted' | chpasswd && \
    cp /etc/passwd /jail/etc/
    
COPY ./run.sh /root/
COPY ./sshd_config /etc/ssh/
# End

# Copying binary to interact with host
WORKDIR /jail/

RUN cp bin/cloud_cat bin/cloud_list && \
    cp bin/cloud_cat bin/cloud_create && \
    cp bin/cloud_cat bin/cloud_mv
# End

# Copy server to docker
WORKDIR /server/
COPY server/receiver.py .
RUN mkdir restricted_user/ && \
    chown gaoler:gaoler restricted_user/
# End

# Custom motd :D
COPY ./motd /etc/
# End

ENTRYPOINT ["sh","/root/run.sh"]