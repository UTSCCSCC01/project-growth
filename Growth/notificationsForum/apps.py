''' Django notificationsForum apps file '''
# -*- coding: utf-8 -*-
from django.apps import AppConfig


class Config(AppConfig):
    name = "notificationsForum"

    def ready(self):
        super(Config, self).ready()
        # this is for backwards compability
        import notificationsForum.signals
        notificationsForum.notify = notificationsForum.signals.notify
