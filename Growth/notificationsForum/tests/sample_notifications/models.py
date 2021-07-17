from django.db import models
from notificationsForum.base.models import AbstractNotification


class NotificationForum(AbstractNotification):
    details = models.CharField(max_length=64, blank=True, null=True)

    class Meta(AbstractNotification.Meta):
        abstract = False
