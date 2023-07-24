from django.urls import path, include

urlpatterns = [
    path('', include((
        'apps.announcement.urls',
        'announcement'
    ),
        namespace='announcement'
    )),
    path('', include((
        'apps.user.urls',
        'user'
    ),
        namespace='user'
    )),
    path('', include((
        'apps.authentication.urls',
        'authentication'
    ),
        namespace='authentication'
    ))
]
