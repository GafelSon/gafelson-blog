from django.db import models
from django.utils import timezone
from ..models.post import PostStatus


class PostManager(models.Manager):
    def get_queryset(self):
        queryset = super().get_queryset()

        now = timezone.now()
        scheduled_posts = queryset.filter(
            status=PostStatus.DRAFT.value,
            published__lte=now
        )
        if scheduled_posts.exists():
            scheduled_posts.update(status=PostStatus.PUBLISHED.value)
            
        return queryset