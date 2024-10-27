# Base image
FROM debian:11-slim

# Set working directory
WORKDIR /app/

# Install necessary packages
RUN apt-get update && \
    apt-get install -y socat python3 python3-pip netcat nginx python3-dotenv cron

# Copy application files
COPY ./names/ /app/names
COPY ./engine/   /app/engine
COPY ./server.py /app/
COPY ./entry.sh /app/
COPY ./requirements.txt /app/
COPY ./static/ /var/www/html/static
COPY ./templates/index.html /var/www/html/index.html
COPY ./templates/review.html /app/
COPY ./env /app/.env

# Setup cleanup cron
RUN echo "* * * * * find /var/www/html -type f -mmin +10 -name '?????????????????????????????????????' -exec rm {} \;" > /etc/cron.d/my_cron_job && \
    chmod 0644 /etc/cron.d/my_cron_job && \
    touch /var/log/cron.log

# Create user and group for running the application
RUN groupadd ctf && \
    useradd -G ctf --home=/app player && \
    chown root:ctf /var/www/html && chmod g+w /var/www/html && \
    mkdir /app/champions && chown root:ctf /app/champions && chmod g+w /app/champions && \
    chown root:ctf /app && chmod g+w /app && \
    chown root:ctf /var/log && chmod g+w /var/log

# Install Python dependencies
RUN pip3 install -r /app/requirements.txt

# Set permissions for scripts
RUN chmod 4755 /app/server.py && \
    chmod 4755 /app/entry.sh

# Expose the ports for netcat and Nginx
EXPOSE 80 ${LISTEN_PORT}

# Configure Nginx
RUN echo "daemon off;" >> /etc/nginx/nginx.conf  # Keep nginx in foreground

# Define entrypoint script to start services
ENTRYPOINT ["/app/entry.sh"]
