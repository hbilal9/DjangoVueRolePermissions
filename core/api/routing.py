from django.urls import path
from .consumers.TestConsumer import TestConsumer

websocket_urlpatterns = [
    path('ws/socket-test/<str:username>/', TestConsumer.as_asgi()),
]

