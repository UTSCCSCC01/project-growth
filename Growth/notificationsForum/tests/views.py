''' Django notificationsForum views for tests '''
# -*- coding: utf-8 -*-
import random

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from notificationsForum.signals import notify


@login_required
def live_tester(request):
    notify.send(sender=request.user, recipient=request.user, verb='you loaded the page')

    return render(request, 'test_live.html', {
        'unread_count': request.user.notificationsForum.unread().count(),
        'notificationsForum': request.user.notificationsForum.all()
    })


def make_notification(request):

    the_notification = random.choice([
        'reticulating splines',
        'cleaning the car',
        'jumping the shark',
        'testing the app',
        'attaching the plumbus',
    ])

    notify.send(sender=request.user, recipient=request.user,
                verb='you asked for a notificatonForum - you are ' + the_notification)
