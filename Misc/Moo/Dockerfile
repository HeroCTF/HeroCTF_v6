FROM debian:12-slim

ENV DEBIAN_FRONTEND noninteractive

# Install dependecies
RUN apt update && apt install openssh-server sudo cowsay vim iperf -y

# Setup user
RUN adduser --disabled-password --gecos "" user && \
    echo 'user:password' | chpasswd && \
    ln -sf /dev/null /home/user/.bash_history && \
    echo 'user ALL=(root) NOPASSWD: /bin/cat /flag.txt' > /etc/sudoers.d/user && \
    chmod 0440 /etc/sudoers.d/user

# Setup rbash
RUN mkdir /usr/local/rbin
COPY challenge/rbash /usr/local/rbin/rbash
COPY challenge/rvim /usr/local/rbin/vim
COPY challenge/vimrc /home/user/.vimrc
RUN chmod +x /usr/local/rbin/rbash && \
    chmod +x /usr/local/rbin/vim && \
    usermod -s /usr/local/rbin/rbash user && \
    ln -s /bin/ls /usr/local/rbin/ls && \
    ln -s /usr/games/cowsay /usr/local/rbin/cowsay && \
    ln -s /usr/bin/dircolors /usr/local/rbin/dircolors && \
    chmod 444 /home/user/.bashrc /home/user/.vimrc /home/user/.profile

# Fix problems
RUN echo "export LC_ALL=C" >> /home/user/.bashrc

# Write flag
RUN echo "Hero{s0m3_s4cr3d_c0w}" > /flag.txt && \
    chown root:root /flag.txt && chmod 400 /flag.txt

# Copy starup file to container and run it
COPY challenge/start.sh /root/start.sh
RUN chmod +x /root/start.sh
EXPOSE 22
CMD ["/root/start.sh"]