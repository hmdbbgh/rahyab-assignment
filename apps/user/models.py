from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from utils.models import TimeStampedModel


User = get_user_model()


class Profile(TimeStampedModel):

    user = models.OneToOneField(
        User,
        related_name="profile",
        verbose_name=_('User'),
        on_delete=models.CASCADE
    )
    announcements_count = models.PositiveIntegerField(
        _("Announcements Count"),
        default=0
    )
    bio = models.CharField(
        _("Bio"),
        max_length=1000,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.user.username

    def __repr__(self):
        return self.user.username
