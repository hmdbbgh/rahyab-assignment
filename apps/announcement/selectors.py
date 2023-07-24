from django.core.cache import cache
from django.db.models import QuerySet

from .models import Announcement


def get_announcements() -> QuerySet[Announcement]:
    """
    Get all accepted announcements from the database.

    Returns:
        QuerySet[Announcement]: A queryset containing all the Accepted Announcement model instances.
    """
    return Announcement.objects.filter(accepted=True)


def get_announcement(*, pk: int) -> Announcement | None:
    """
    Get a accepted announcements from the database by pk .
    Return None if pk is invalid

    Returns:
        Announcement: A Accepted Announcement model instances.
        None: if pk is invalid
    """
    try:
        return get_announcements().get(pk=pk)
    except:
        return None


def search_announcements(*, search_text: str) -> QuerySet[Announcement]:
    announcements = Announcement.objects.filter(
        accepted=True,
        title__icontains=search_text
    )

    return announcements


def get_announcement_views_count(
    *,
    pk: int,
):
    current_value = cache.get(f'announcement:{pk}:views')
    if current_value is None:
        announcement = get_announcement(pk=pk)
        if announcement:
            current_value = announcement.views_count

    return current_value
