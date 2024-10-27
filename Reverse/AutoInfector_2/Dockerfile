FROM python:3.12-alpine

WORKDIR /app

COPY ./app.py .
COPY ./stage2.au3 .

RUN python3 -m pip install flask

EXPOSE 5000
ENTRYPOINT ["python3", "app.py"]