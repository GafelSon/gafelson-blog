from .base import *

# Security
DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# DATABASES
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# DEBUG TOOLBAR
DEBUG_TOOLBAR_PANELS = [
    "debug_toolbar.panels.history.HistoryPanel",
    "debug_toolbar.panels.timer.TimerPanel",
    "debug_toolbar.panels.headers.HeadersPanel",
    "debug_toolbar.panels.request.RequestPanel",
    "debug_toolbar.panels.sql.SQLPanel",
    "debug_toolbar.panels.cache.CachePanel",
]

# Static files
MEDIA_ROOT = BASE_DIR / "media"
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
COMPRESS_ROOT = STATIC_ROOT
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
COMPRESS_OFFLINE = True


# Email settings
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
