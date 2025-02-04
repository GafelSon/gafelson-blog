from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.cache import cache

# TODO: Import your Post model and Telegram settings
# from .models import Post
# from django.conf import settings


# Cache invalidation signal
@receiver(post_save, sender="blog.Post")
def invalidate_post_cache(sender, instance, **kwargs):
    """Clear cache when a post is saved or updated"""
    cache.delete("post_years")
    # TODO: Add other cache keys to invalidate


# TODO: Telegram notification signal
@receiver(post_save, sender="blog.Post")
def send_to_telegram(sender, instance, created, **kwargs):
    """Send new blog posts to Telegram channel

    Future implementation:
    1. Check if post is published and public
    2. Format post content for Telegram
    3. Add post URL and metadata
    4. Send to Telegram channel using bot API
    5. Handle errors and retries
    6. Add logging
    """
    if created and instance.is_published:
        # TODO: Implement Telegram bot integration
        # - Configure bot token and channel ID
        # - Format message with title, subtitle, URL
        # - Add preview image if available
        # - Send using telegram-python-bot
        pass


# TODO: Pre-save signal for post processing
@receiver(pre_save, sender="blog.Post")
def process_post_content(sender, instance, **kwargs):
    """Process post content before saving

    Future implementation:
    1. Generate post preview
    2. Process markdown/content
    3. Optimize images
    4. Generate metadata
    """
    pass
