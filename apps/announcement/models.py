from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from utils.models import TimeStampedModel


User = get_user_model()


class Announcement(TimeStampedModel):

    user = models.ForeignKey(
        User,
        verbose_name=_('User'),
        related_name="announcments",
        on_delete=models.CASCADE
    )
    title = models.CharField(
        _("Title"),
        max_length=200
    )
    views_count = models.PositiveIntegerField(
        _("Announcement views count"),
        default=0
    )
    content = models.TextField(_("Content"))
    accepted = models.BooleanField(
        _("Accepted"),
        default=False
    )

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.title
