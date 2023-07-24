from .base import (
    INSTALLED_APPS,
    STATIC_ROOT
)
from datetime import timedelta


# ############## #
#   EXTENSIONS   #
# ############## #
INSTALLED_APPS.extend([
    'rest_framework',
    'django_filters',
    'drf_spectacular',
    'django_celery_results',
    'django_celery_beat',
])

# ############## #
# CUSTOM PROJECT #
# ############## #
INSTALLED_APPS.extend([
    'utils',
    'apps.user.apps.UserConfig',
    'apps.announcement.apps.AnnouncementConfig',
    'apps.authentication.apps.AuthenticationConfig',
    'apps.tasks.apps.TasksConfig',
])

# ###################### #
# EXTENSION DEPENDENCIES #
# ###################### #

ALLOW_UNICODE_SLUGS = True

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

LOGIN_REDIRECT_URL = ''

LOGOUT_REDIRECT_URL = ''


# ###################### #
#     REST FRAMEWORK     #
# ###################### #
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': []
}
