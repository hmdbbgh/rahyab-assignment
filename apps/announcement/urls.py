from django.urls import path

from .apis import (
    UserAnnouncementsAPI,
    AnnouncementAcceptAPI,
    AnnouncementDetailAPI,
    AnnouncementSearchAPI,
    AnnouncementViewsCountAPI,
    AnnouncementListCreateAPI,
)


app_name = "apps.announcement"


urlpatterns = [
    path(
        'my-announcements/',
        UserAnnouncementsAPI.as_view(),
        name='my-announcements'
    ),
    path(
        'announcements/',
        AnnouncementListCreateAPI.as_view(),
        name='create-list'
    ),
    path(
        'announcements/<int:announcement_id>/',
        AnnouncementDetailAPI.as_view(),
        name='detail'
    ),
    path(
        'announcements/<int:announcement_id>/accept/',
        AnnouncementAcceptAPI.as_view(),
        name='accept'
    ),
    path(
        'announcements/<int:announcement_id>/views/',
        AnnouncementViewsCountAPI.as_view(),
        name='views-count'
    ),
    path(
        'announcements/search/',
        AnnouncementSearchAPI.as_view(),
        name='search'
    ),
]
