import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import chat.routing # Import our new chat routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'senior_companion_project.settings')

# This is the old, default application
# application = get_asgi_application()

# This is our new application router
application = ProtocolTypeRouter({
    "http": get_asgi_application(), # Standard HTTP requests
    "websocket": AuthMiddlewareStack( # WebSocket requests
        URLRouter(
            chat.routing.websocket_urlpatterns # Send them to our chat router
        )
    ),
})