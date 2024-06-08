"""
ASGI config for messenger project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
import django

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from messagese.routing import websocket_urlpatterns
from channels.security.websocket import AllowedHostsOriginValidator
#from channels.routing import get_default_application

#django.setup()
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

#application = get_asgi_application()
#application = get_default_application()
application = ProtocolTypeRouter({'websocket': AllowedHostsOriginValidator(AuthMiddlewareStack(URLRouter(websocket_urlpatterns))),
                                  'http': get_asgi_application()})