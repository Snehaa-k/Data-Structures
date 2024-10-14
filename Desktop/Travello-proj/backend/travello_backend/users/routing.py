from django.urls import path
from .consumer import TravelChat,NotificationConsumer
from django.urls import re_path

websocket_urlpatterns = [
     re_path(r'ws/chat/?$', TravelChat.as_asgi()),
     re_path(r'ws/notification/?$', NotificationConsumer.as_asgi()), 
]