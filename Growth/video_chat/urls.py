from django.urls import path
from .views import peer, peerA, peerB

urlpatterns = [
    path('', peer, name='peer'),
    path('peerA/', peerA, name='peerA'),
    path('peerB/', peerB, name='peerB'),
]