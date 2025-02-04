from django.apps import AppConfig
from django.db.models import BigAutoField
from typing import ClassVar


class BlogConfig(AppConfig):
    """
    📚 Gaf Blog Application Configuration

    Handles app-specific settings and initialization
    More than just metadata - your app's launchpad! 🚀
    """

    # 🔐 Database field type for model PKs (Django 3.2+ default)
    default_auto_field: ClassVar[str] = "django.db.models.BigAutoField"

    # 🏷️ Python path to application (auto-detected if using default AppConfig)
    name: str = "blog"

    # 🌐 Human-readable name for admin (optional but recommended)
    verbose_name: str = "Blog Gaf"

    # ⚡ App initialization hook (great for signals registration!)
    def ready(self) -> None:
        """
        Called when Django starts. Perfect for:
        - Connecting signals 📡
        - Registering checks ✔️
        - Scheduled tasks setup ⏰
        """
        # Example (uncomment when needed):
        # from . import signals  # noqa: F401
        super().ready()
