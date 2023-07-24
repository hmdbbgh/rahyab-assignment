from celery import shared_task

from .services import save_views_count_to_db


@shared_task
def save_views_count_to_db_task() -> None:
    save_views_count_to_db()
