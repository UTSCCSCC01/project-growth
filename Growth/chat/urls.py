from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    url(r'^entryChat/', views.entryChat, name='entryChat'),
    path('<str:room_name>/', views.room, name='room'),
]
