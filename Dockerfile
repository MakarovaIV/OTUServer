# syntax=docker/dockerfile:1

FROM python:3.10.11-alpine3.17

WORKDIR /app

COPY . .

USER root

CMD ["python3", "httpd.py", "-a", "0.0.0.0", "-p", "80"]
