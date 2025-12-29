FROM python:3.11-slim

# отключаем .pyc и буферизацию логов
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# системные зависимости
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# poetry
RUN pip install --upgrade pip \
    && pip install poetry

# зависимости
COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# код
COPY . .

EXPOSE 8000
