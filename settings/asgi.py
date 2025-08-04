"""
ASGI config for settings project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from strawberry.channels import GraphQLProtocolTypeRouter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.settings')
print("🚀 ASGI application loaded")
django_asgi_app = get_asgi_application()

# Import your Strawberry schema after creating the django ASGI application
# This ensures django.setup() has been called before any ORM models are imported
# for the schema.
from api.schema import schema

application = GraphQLProtocolTypeRouter(
    schema,
    django_application=django_asgi_app,
)
