from django.db import models
from django.utils import timezone


class PostManager(models.Manager):
    """Custom query machinery for post operations"""

    def published(self):
        """Get currently active published posts"""
        return self.filter(
            status=PostStatus.PUBLISHED.value, published__lte=timezone.now()
        )
