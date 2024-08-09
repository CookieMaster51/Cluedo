FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update                 \
    && apt-get upgrade -y          \
    && apt-get clean               \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /cluedo
COPY app .

CMD ["python3", "main.py"]