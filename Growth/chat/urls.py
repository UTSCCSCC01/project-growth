from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    url(r'^$', views.entryChat, name='entryChat'),
    path('<str:room_name>/', views.room, name='room'),
    path('<str:room_name>/', views.peer, name='peer'),
    url(r'^peerA/', views.peerA, name='peerA'),
    url(r'^peerB/', views.peerB, name='peerB'),
]
