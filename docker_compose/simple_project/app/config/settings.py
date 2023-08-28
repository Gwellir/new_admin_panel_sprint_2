"""Основной модуль настроек djangо приложения movies_admin."""

import os
from pathlib import Path

from dotenv import load_dotenv
from split_settings.tools import include

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = os.environ.get('DEBUG', False) == 'True'

ALLOWED_HOSTS = tuple(os.environ.get('ALLOWED_HOSTS').split(','))


include(
    'components/application.py',
    'components/database.py',
    'components/password_validation.py',
    'components/internationalization.py',
    'components/static_files.py',
    'components/default_auto_field.py',
)
