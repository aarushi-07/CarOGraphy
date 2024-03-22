"""
ASGI config for CarOGraphy project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack

import CarOGraphy
import myapp.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CarOGraphy.settings')

application = ProtocolTypeRouter(
    {
        'http': get_asgi_application(),
        'websocket': AuthMiddlewareStack(
            URLRouter(
                myapp.routing.websocket_urlpatterns
            )
        )
    }
)
