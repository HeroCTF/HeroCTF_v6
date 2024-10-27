FROM sagemath/sagemath:latest

RUN sudo apt update -y && sudo apt install -y socat

COPY --chown=sage . .

RUN chmod 755 entry.sh chall.sage

EXPOSE ${LISTEN_PORT}

ENTRYPOINT ["/home/sage/entry.sh"]