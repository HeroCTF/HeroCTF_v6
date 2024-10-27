FROM node:latest

WORKDIR /app/

# Sorry for that, carbone js library requires libreoffice to work
RUN apt update && \
    apt install libxinerama1 libfontconfig1 libdbus-glib-1-2 libcairo2 libcups2 libglu1-mesa libsm6 netcat-traditional gcc -y && \
    wget https://downloadarchive.documentfoundation.org/libreoffice/old/7.5.1.1/deb/x86_64/LibreOffice_7.5.1.1_Linux_x86-64_deb.tar.gz && \
    tar -zxvf LibreOffice_7.5.1.1_Linux_x86-64_deb.tar.gz && \
    rm LibreOffice_7.5.1.1_Linux_x86-64_deb.tar.gz && \
    cd LibreOffice_7.5.1.1_Linux_x86-64_deb/DEBS && \
    dpkg -i *.deb && \
    mkdir /tmp/files && \
    chmod 777 /tmp/files/

WORKDIR /build/
COPY getflag.c .
RUN gcc getflag.c -o getflag && \
    mv getflag / && \
    chmod u+s /getflag
COPY ./flag.txt /root/

WORKDIR /app/

COPY ./odt_templates/ /tmp/files/

COPY ./src/ .

RUN npm i --omit=dev && npm cache clean --force && \
    rm -fr /build/ && \
    chown -R node:node /app/

EXPOSE 3000

USER node

CMD ["node","index.js"]