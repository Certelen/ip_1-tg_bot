# Бот для тестового задания
## Описание
Бот позволяет просмотреть список категорий, подкатегорий, товаров, добавить товар в корзину, купить его, увидеть список популярных вопросов, получить заказ в гугл-таблицу.

## Технологии
- Python 3.11
- Django 4.2.7
- Aiogram 3.1.1
- Aiogoogle 5.7.0
- PostgreSQL 13.0
- Nginx 1.21.3
- Docker
- Docker-compose
- Docker Hub

# Установка
## Копирование репозитория
Клонируем репозиторий
```
~ git clone git@github.com:Certelen/ip_1-tg_bot.git
```
По инструкции на сайте [google API](https://developers.google.com/sheets/api/quickstart/python?hl=en) создать json-ключ.
На боевом сервере создайте файл .env в папке telegram и backend и заполните его:
telegram
```
- TG_TOKEN = <Токен бота, можно получить у BotFather>
- ADMIN_ID = <ID телеграмм-аккаунта админа>
- PROVIDER_TOKEN = <Токен платежной системы>
- SPREAD_ID= <id гугл-таблицы с заказами, нужно дать доступ по ссылке с правами редактора>

- DB_NAME = postgres
- DB_USERNAME = postgres
- DB_PASSWORD = postgres
- DB_HOST = db
- DB_PORT = 5432

- GMAIL = <gmail-почта от которой выпущен json-ключ>
- TYPE = <значение из json-ключа>
- PROJ_ID = <значение из json-ключа>
- KEY_ID = <значение из json-ключа>
- KEY = <значение из json-ключа>
- CLIENT_MAIL = <значение из json-ключа>
- CLIENT_ID = <значение из json-ключа>
- AUTH_URL = <значение из json-ключа>
- TOKEN_URL = <значение из json-ключа>
- AUTH_X509 = <значение из json-ключа>
- CLIENT_X509 = <значение из json-ключа>
```

backend
```
- SECRET_KEY=<SECRET_KEY>

- POSTGRES_DB = postgres
- POSTGRES_USER = postgres
- POSTGRES_PASSWORD = postgres
- POSTGRES_HOST = db
- POSTGRES_PORT = 5432

```

## Развертывание проекта с помощью Docker:
Разворачиваем контейнеры в фоновом режиме из папки infra:
```
sudo docker compose up -d
```
При первом запуске выполняем миграции:
```
sudo docker compose exec backend python manage.py migrate
```
И собираем статику:
```
sudo docker compose exec backend python manage.py collectstatic --no-input
```
Создаем суперпользователя:
```
sudo docker compose exec backend python manage.py createsuperuser
```

# Адресные пути
- [Админ-панель базы данных](http://127.0.0.1/admin)
