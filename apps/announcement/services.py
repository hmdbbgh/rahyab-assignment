from django.core.cache import cache
from django.contrib.auth import get_user_model

from .models import Announcement


User = get_user_model()


def create_announcement(
    *,
    user: User,
    title: str,
    content: str
) -> Announcement:
    return Announcement.objects.create(
        user=user,
        title=title,
        content=content
    )


def update_announcement(
    *,
    announcement: Announcement,
    title: str | None,
    content: str | None
) -> Announcement:

    if title:
        announcement.title = title
    if content:
        announcement.content = content
    announcement.save()

    return announcement


def delete_announcement(*, announcement: Announcement) -> bool:
    deleted_count, _ = announcement.delete()
    return bool(deleted_count)


def increment_announcement_views_count(
    *,
    pk: int,
    increment_value: int = 1,
    timeout: int | None = None
) -> int:
    """
    Increments the value of the cache announcement id by the specified increment_value or adds a new announcement if it doesn't exist.

    Args:
        pk (int): The announcement id to increment or add.
        increment_value (int): The value to increment the cache announcement. Default is 1.
        timeout (int): The cache timeout for the pk in seconds. Default is None (no timeout).

    Returns:
        int: The updated value of the cache announcement after incrementing or adding.
    """
    current_value = cache.get(f'announcement:{pk}:views')
    if current_value is not None:
        new_value = current_value + increment_value
    else:
        announcement = Announcement.objects.get(pk=pk)
        new_value = announcement.views_count + increment_value

    cache.set(f'announcement:{pk}:views', new_value, timeout)

    return new_value


def save_views_count_to_db() -> None:

    keys = cache.keys("announcement:*:views")
    for key in keys:
        try:
            announcement_id = int(key.split(":")[1])
            views_count = int(cache.get(key))
            announcement = Announcement.objects.get(pk=announcement_id)
            announcement.views_count = views_count
            announcement.save()
        except Exception as e:
            print(e)
            continue
            # TODO: can add log to logging
