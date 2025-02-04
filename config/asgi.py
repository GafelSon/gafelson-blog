import os
from django.core.asgi import get_asgi_application
from django.conf import settings

# Set default Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# Initialize ASGI application with lifespan protocol support
application = get_asgi_application()

# ASGI Middleware Stack Optimization 🚀
if not settings.DEBUG:
    from whitenoise.middleware import WhiteNoiseMiddleware
    from middleware.security import SecurityHeadersMiddleware
    from asgi_correlation_id import CorrelationIdMiddleware

    # Wrap application with production middleware
    application = WhiteNoiseMiddleware(application)
    application = SecurityHeadersMiddleware(application)
    application = CorrelationIdMiddleware(application)

# Optional: Add WebSocket support (if using Django Channels)
# from channels.routing import ProtocolTypeRouter
# application = ProtocolTypeRouter({
#     "http": application,
#     "websocket": AuthMiddlewareStack(URLRouter(...)),
# })
