

from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # Make sure your path does NOT have 'ws/' at the start
    re_path(
        r'^chat/(?P<user_1_id>\d+)/(?P<user_2_id>\d+)/$', 
        consumers.ChatConsumer.as_asgi()
    ),
]