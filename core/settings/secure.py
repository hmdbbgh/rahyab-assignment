import os
from .base import BASE_DIR
from decouple import config


SECRET_KEY = config('SECRET_KEY')

PREPEND_WWW = config('PREPEND_WWW', cast=bool)
APPEND_SLASH = config('APPEND_SLASH', cast=bool)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT', cast=int),
        'TEST': {
            'NAME': config('DB_TEST'),
        },
    }
}


# ######################### #
#      UPLOAD SETTING       #
# ######################### #

FILE_UPLOAD_TEMP_DIR = config('FILE_UPLOAD_TEMP_DIR')
FILE_UPLOAD_PERMISSIONS = 0o755
FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o755
FILE_UPLOAD_MAX_MEMORY_SIZE = config('FILE_UPLOAD_MAX_MEMORY_SIZE', cast=int)
MAX_UPLOAD_SIZE = config('MAX_UPLOAD_SIZE', cast=int)


# ######################### #
#           REDIS           #
# ######################### #
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': config(
            "REDIS_LOCATION",
            default="redis://localhost:6379"
        ),
    }
}
CACHE_TTL = 60 * 15


# ######################### #
#          CELERY           #
# ######################### #
CELERY_TASK_ALWAYS_EAGER = True
CELERY_BROKER_BACKEND = "memory"
CELERY_TASK_EAGER_PROPAGATES = True

CELERY_BROKER_URL = config(
    'CELERY_BROKER_URL',
    default='amqp://guest:guest@localhost:5672//'
)

CELERY_TIMEZONE = 'UTC'
CELERT_TASK_TIME_LIMIT = 30  # seconds
CELERY_TASK_MAX_RETRIES = 3
CELERY_TASK_SOFT_TIME_LIMIT = 20  # seconds

CELERY_RESULT_BACKEND = 'django-db'
CELERY_BEAT_SCHEDULE = {
    'notify_customers': {
        'task': 'config.tasks.notify_customers',
        'schedule': 500,
        'args': ['Hello World'],
    }
}
