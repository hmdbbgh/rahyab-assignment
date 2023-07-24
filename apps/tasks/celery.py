import os
from celery import Celery
from decouple import config

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    f'core.settings.{"development" if config("DEBUG") else "production"}'
)

celery = Celery('config')
celery.config_from_object('django.conf:django', namespace='CELERY')
celery.autodiscover_tasks()
