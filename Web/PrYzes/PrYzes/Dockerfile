FROM python:3.12-bookworm

WORKDIR /app

COPY src/ /app/

RUN python3 -m pip install Flask

CMD ["python3", "/app/app.py"]