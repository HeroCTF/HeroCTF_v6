FROM alpine:3.17.0

# Init
RUN apk update && \
    apk add --no-cache gcc libc-dev python3 py3-pip && \
# Create user
    adduser -D -u 1000 challenge && \
    echo "challenge:$(head -c 32 /dev/urandom | base64)" | chpasswd

#Setup flag
WORKDIR /root/
COPY getflag.c .
RUN gcc getflag.c -o getflag && \
    chmod u+s getflag && \
    mv getflag ../ && \
    rm getflag.c
COPY flag.txt .

#Setup webapp
WORKDIR /app/
COPY ./challenge/ .
RUN pip3 install -r requirements.txt

USER challenge

CMD ["python3","/app/app.py"]
