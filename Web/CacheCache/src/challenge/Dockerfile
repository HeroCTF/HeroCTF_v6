FROM alpine:3.20.3

WORKDIR /usr/app
COPY ./src/ .
RUN apk add --update --no-cache python3 py3-pip chromium-chromedriver       && \
    pip install --no-cache-dir --break-system-packages -r requirements.txt

USER guest
CMD ["/usr/bin/python3", "/usr/app/app.py"]
