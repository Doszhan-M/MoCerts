import os
from pathlib import Path
from colorama import Fore, Style

HOST = 'http://doszhan.space'

BASE_DIR = Path(__file__).resolve().parent.parent

try:
    with open(os.path.join(BASE_DIR, 'secret/SECRET_KEY.txt'), 'r') as token:
        secret = token.read()
    SECRET_KEY = secret  # адрес сервера почты для всех один и тот же
except FileNotFoundError:
    print(Fore.RED + 'Не найден файл для SECRET_KEY')
    print(Style.RESET_ALL)
    SECRET_KEY = 'sefesfsefsefsfesff'

DEBUG = False

ALLOWED_HOSTS = ['doszhan.space', 'localhost', '127.0.0.1']

# Настройки для базы данных 
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


STATIC_ROOT = os.path.join(BASE_DIR, 'static')
