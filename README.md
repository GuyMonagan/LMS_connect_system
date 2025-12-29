# LMS_connect_system
### LMS-система, в которой каждый желающий может размещать свои полезные материалы или курсы.


## LMS System API

Учебный проект по Django + Django REST Framework.
Реализованы курсы, уроки, пользователи и платежи с фильтрацией.

## Стек

- Python 3.11 
- Django 5.x 
- Django REST Framework 
- PostgreSQL 
- Postman для тестирования API
- Docker

## Запуск проекта через Docker

1. Клонировать проект
```
git clone https://github.com/GuyMonagan/LMS_connect_system
cd LMS_connect_system
```

2. Создайте файл `.env` на основе `.env.example` и заполните необходимые переменные


3. Запуск сервисов

```
docker compose up --build
```

После запуска будут доступны сервисы:
- Django backend — http://localhost:8000
- PostgreSQL — внутри Docker
- Redis — брокер Celery
- Celery worker и Celery Beat


## Загрузка тестовых данных (опционально)

Для загрузки фикстур можно выполнить команды:

```bash
docker compose exec web python manage.py loaddata payments/fixtures/users_fixture.json
docker compose exec web python manage.py loaddata payments/fixtures/courses_fixture.json
docker compose exec web python manage.py loaddata payments/fixtures/lessons_fixture.json
docker compose exec web python manage.py loaddata payments/fixtures/payments_fixture.json
```

## Deployment

Проект использует Docker и GitHub Actions для автоматического деплоя.

- `docker-compose.yml` — для локальной разработки
- `docker-compose.prod.yml` — для продакшн-деплоя

После успешного прохождения тестов GitHub Actions:
- собирает Docker-образ
- публикует его в registry
- деплоит на сервер через SSH


## CI/CD

Проект использует GitHub Actions для CI/CD.

Pipeline:
- запуск тестов
- сборка Docker-образа
- публикация в GitHub Container Registry
- деплой на сервер по SSH

Для локальной разработки используется `docker-compose.yml`,
для продакшн-деплоя — `docker-compose.prod.yml`.


## Функциональность проекта

Курсы (ViewSet)
- GET /api/courses/ — список курсов 
- POST /api/courses/ — создать курс 
- GET /api/courses/<id>/ — получить курс 
- PUT/PATCH /api/courses/<id>/ — обновить 
- DELETE /api/courses/<id>/ — удалить

Дополнительно:
- вывод количества уроков (lessons_count)
- вложенный список уроков (lessons)

Уроки (GenericAPIView)
- GET /api/lessons/ 
- POST /api/lessons/ 
- GET /api/lessons/<id>/ 
- PUT/PATCH /api/lessons/<id>/ 
- DELETE /api/lessons/<id>/

Пользователи
- GET /api/users/<id>/ — профиль 
- PUT/PATCH /api/users/<id>/ — обновление профиля

Дополнительно:
- вывод истории платежей пользователя

Платежи
- GET /api/payments/ — список
- Фильтры:
- - ?ordering=payment_date 
- - ?course=<id>
- - ?lesson=<id>
- - ?payment_method=cash|transfer

## Структура проекта

- materials — модели курсов и уроков 
- users — кастомная модель пользователя 
- payments — платежи + фильтрация + фикстуры 
- config — настройки, маршрутизация


## Celery + Redis интеграция

- Подключён Celery для асинхронной обработки задач. 
- Использован Redis как брокер сообщений. 
- Настроен Celery Beat для периодических задач. 
- Реализована рассылка email подписчикам при обновлении курса. 
- Добавлена фоновая задача: авто-блокировка пользователей, не заходивших более 30 дней. 
- Написаны соответствующие unit-тесты.