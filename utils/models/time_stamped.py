from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedModel(models.Model):

    created_at = models.DateTimeField(
        _("اضافه شده در"),
        auto_now_add=True
    )

    modified_at = models.DateTimeField(
        _("اصلاح شده در"),
        auto_now=True
    )

    class Meta:

        abstract = True
