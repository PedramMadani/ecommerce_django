import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import Bookamin_store.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Bookamin_store.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            Bookamin_store.routing.websocket_urlpatterns
        )
    ),
})
