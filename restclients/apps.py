from django.apps import AppConfig
from django.conf import settings


class RestClientsAppConfig(AppConfig):
    name = 'restclients'

    if 'rc_django' not in settings.INSTALLED_APPS:
        settings.INSTALLED_APPS += ('rc_django', )
