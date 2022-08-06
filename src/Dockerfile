FROM python:3.10.5-slim

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt update\
  && apt install gcc -y\
  && pip install --upgrade pip\
  && pip install poetry==1.1.6

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
  && poetry install --no-dev --no-interaction --no-ansi

COPY . .

ENTRYPOINT ["python", "main.py"]