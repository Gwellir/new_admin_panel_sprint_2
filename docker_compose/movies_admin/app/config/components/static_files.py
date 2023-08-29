"""Настройки статических файлов для приложения movies_admin."""
import os

from config.settings import BASE_DIR

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / os.environ.get('STATIC_ROOT', 'static')
