import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = 'true'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'studentflow.settings')

django_asgi_application = get_asgi_application()

from studentflow.chat.middleware import TokenAuthMiddleware
from studentflow.chat import routing

application = ProtocolTypeRouter({
    'http': django_asgi_application,
    'websocket': AllowedHostsOriginValidator(
        TokenAuthMiddleware(URLRouter(routing.websocket_urlpatterns))
    ),
})
