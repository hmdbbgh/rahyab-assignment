from django.urls import path, include

urlpatterns = [
    path('', include(('apps.authentication.urls', 'authentication'))),
    path('', include(('apps.user.urls', 'user'))),
]
