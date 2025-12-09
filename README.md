# LMS_connect_system
### LMS-система, в которой каждый желающий может размещать свои полезные материалы или курсы.


## LMS System API

Учебный проект по Django + Django REST Framework.
Реализованы курсы, уроки, пользователи и платежи с фильтрацией.

## Стек

- Python 3.11 
- Django 4.x 
- Django REST Framework 
- PostgreSQL 
- Postman для тестирования AP

## Установка и запуск

1. Клонировать проект
```
git clone https://github.com/GuyMonagan/LMS_connect_system
cd LMS_connect_system
```

2. Установить зависимости

```
poetry install
```

3. Настроить переменные окружения

Создать файл .env:

```
POSTGRES_DB=lms_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
SECRET_KEY=django-insecure-123

```

4. Применить миграции

```
poetry run python manage.py migrate
```

5. Загрузить тестовые данные (фикстуры)

```
poetry run python manage.py loaddata payments/fixtures/users_fixture.json
poetry run python manage.py loaddata payments/fixtures/courses_fixture.json
poetry run python manage.py loaddata payments/fixtures/lessons_fixture.json
poetry run python manage.py loaddata payments/fixtures/payments_fixture.json

```

6. Запуск сервера

```
poetry run python manage.py runserver
```

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


## Выполненные требования

- ViewSet для курса 
- Generic-классы для уроков 
- Доп. поле количества уроков 
- Модель Payment 
- Фикстуры 
- Вложенный вывод уроков 
- Фильтрация платежей 
- История платежей в профиле 
- PostgreSQL 
- namespace для приложений 
- User без username
---


## Celery + Redis интеграция

- Подключён Celery для асинхронной обработки задач. 
- Использован Redis как брокер сообщений. 
- Настроен Celery Beat для периодических задач. 
- Реализована рассылка email подписчикам при обновлении курса. 
- Добавлена фоновая задача: авто-блокировка пользователей, не заходивших более 30 дней. 
- Написаны соответствующие unit-тесты.