import os

from dotenv import load_dotenv

load_dotenv()

PROVIDER_TOKEN = os.getenv('PROVIDER_TOKEN', '')
TG_TOKEN = os.getenv('TG_TOKEN', '')
ADMIN_ID = os.getenv('ADMIN_ID', '')
SECRET = os.getenv('SECRET', '')
SPREAD_ID = os.getenv('SPREAD_ID', '')

"""Данные для БД"""
DB_NAME = os.getenv('DB_NAME', 'postgres')
DB_USERNAME = os.getenv('DB_USERNAME', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
HOST = os.getenv('HOST', 'http://127.0.0.1:8000/')

SQLALCHEMY_DATABASE_URL = ((
    f'postgresql+asyncpg://\
{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
))

"""Данные для GoogleAPI"""
GMAIL = os.getenv('GMAIL')
TYPE = os.getenv('TYPE')
PROJ_ID = os.getenv('TYPE')
KEY_ID = os.getenv('KEY_ID')
KEY = os.getenv('KEY').replace(r'\n', '\n')
CLIENT_MAIL = os.getenv('CLIENT_MAIL')
CLIENT_ID = os.getenv('CLIENT_ID')
AUTH_URL = os.getenv('AUTH_URL')
TOKEN_URL = os.getenv('TOKEN_URL')
AUTH_X509 = os.getenv('AUTH_X509')
CLIENT_X509 = os.getenv('CLIENT_X509')

"""Настройки"""
PAGINATION_ROW = 2
PAGINATION_WORD_ROW = 2
