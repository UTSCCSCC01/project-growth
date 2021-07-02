from django.conf.urls import url
from .views import peer, peerA, peerB

urlpatterns = [
    url(r'^$', peer, name='peer'),
    url(r'^peerA/', peerA, name='peerA'),
    url(r'^peerB/', peerB, name='peerB'),
]