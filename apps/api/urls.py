from django.urls import path, include

urlpatterns = [
    path('', include(('apps.authentication.urls', 'blog')))
]
