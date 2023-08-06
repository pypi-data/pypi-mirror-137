"""Настройки Django приложения для авторизации через https://cbias.ru."""

from django.apps import AppConfig


class DjangocbiasauthConfig(AppConfig):
    """Класс конфигурации приложения."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_cbias_auth'
