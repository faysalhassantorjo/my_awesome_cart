from django.urls import path
from . import consumers
from django.urls import re_path

websocket_urlpatterns = [
    path('ws/sc/', consumers.MySyncConsumer.as_asgi()),
    re_path(r'ws/ac/$', consumers.MyAsyncConsumer.as_asgi()),
]
