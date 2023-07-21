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
