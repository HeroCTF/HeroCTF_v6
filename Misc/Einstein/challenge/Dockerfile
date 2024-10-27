FROM debian:12-slim

ENV DEBIAN_FRONTEND noninteractive

# Install dependecies
RUN apt update && apt install openssh-server sudo gcc -y

# Setup user
RUN adduser --disabled-password --gecos "" user && \
    echo 'user:password' | chpasswd && \
    ln -sf /dev/null /home/user/.bash_history

RUN adduser --disabled-password --gecos "" einstein && \
    echo 'einstein:7n4MThECq6MSiQQd' | chpasswd && \
    ln -sf /dev/null /home/einstein/.bash_history

# Copy challenge files
COPY --chown=einstein:einstein theory.txt /home/einstein/theory.txt
COPY --chown=einstein:einstein learn.c /home/user/learn.c
RUN gcc /home/user/learn.c -o /home/user/learn && \
    chown einstein:einstein /home/user/learn && \
    chmod +x /home/user/learn && \
    chmod +s /home/user/learn

# Write flag
RUN echo "Hero{th30ry_of_r3l4tiv3_p4th5}" > /home/einstein/flag.txt && \
    chown einstein:einstein /home/einstein/flag.txt && chmod 400 /home/einstein/flag.txt

# Copy starup file to container and run it
COPY start.sh /root/start.sh
RUN chmod +x /root/start.sh
EXPOSE 22
CMD ["/root/start.sh"]