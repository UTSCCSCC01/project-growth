# chat/routing.py
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'peer[AB]/', consumers.VideoConsumer.as_asgi()),
    re_path(r'', consumers.VideoConsumer.as_asgi()),
    re_path(r'ws/video_chat/(?P<room_name>\w+)/$', consumers.VideoConsumer.as_asgi()), #(?P<room_name>\w+)/$
]
