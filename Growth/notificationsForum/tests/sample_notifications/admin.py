import swapper
from django.contrib import admin
from notificationsForum.base.admin import AbstractNotificationAdmin

NotificationForum = swapper.load_model('notificationsForum', 'NotificationForum')


@admin.register(NotificationForum)
class NotificationAdmin(AbstractNotificationAdmin):
    pass
