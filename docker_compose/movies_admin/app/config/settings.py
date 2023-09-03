"""Основной модуль настроек djangо приложения movies_admin."""

import os
from pathlib import Path

from dotenv import load_dotenv
from split_settings.tools import include

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = os.environ.get('DEBUG', False) == 'True'

api_permission = os.environ.get('PERMISSION_REQUIRED', 'is_staff')
PERMISSION_REQUIRED = api_permission if api_permission else []

ALLOWED_HOSTS = tuple(os.environ.get('ALLOWED_HOSTS').split(','))


SPLIT_SUBMODULES = [  # noqa: WPS407
    'components/application.py',
    'components/database.py',
    'components/password_validation.py',
    'components/internationalization.py',
    'components/static_files.py',
    'components/default_auto_field.py',
]

if DEBUG:
    SPLIT_SUBMODULES.append('components/debug.py')

include(*SPLIT_SUBMODULES)
