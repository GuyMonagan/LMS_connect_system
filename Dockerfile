FROM python:3.11-slim

# отключаем .pyc и буферизацию логов
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# рабочая директория
WORKDIR /app

# системные зависимости
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# устанавливаем poetry
RUN pip install --upgrade pip \
    && pip install poetry

# копируем файлы зависимостей
COPY pyproject.toml poetry.lock ./

# отключаем виртуальное окружение poetry (ВАЖНО)
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# копируем весь проект
COPY . .

# порт Django
EXPOSE 8000

# команда по умолчанию (переопределим в docker-compose)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
