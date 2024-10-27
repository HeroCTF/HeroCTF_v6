# Use an official Hugo image from Docker Hub
FROM klakegg/hugo:ext-alpine AS builder

# Set the working directory inside the container
WORKDIR /app

# Copy the Hugo site source files from your local 'src' directory to the container
COPY src/ /app

# Build the Hugo site (output is in the 'public' directory)
RUN hugo

# Start a new stage to serve the Hugo site
FROM alpine:3.12

# Install Nginx to serve the static site
RUN apk add --no-cache nginx

# Set the working directory for Nginx configuration
WORKDIR /usr/share/nginx/html

# Copy the built Hugo site from the previous stage into the Nginx web root
COPY --from=builder /app/public/ /usr/share/nginx/html/

# Expose port 8085 to access the site from the host
EXPOSE 8085

# Create a simple Nginx configuration to listen on port 8085
RUN echo "server { listen 8085; root /usr/share/nginx/html; index index.html; }" > /etc/nginx/conf.d/default.conf

# Create the directory for the nginx.pid file
RUN mkdir -p /run/nginx

# Ensure Nginx runs in the foreground to keep the container alive
CMD ["nginx", "-g", "daemon off;"]

