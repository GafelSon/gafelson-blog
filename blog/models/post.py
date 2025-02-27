from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from .mixins import SEOContentMixin
from .enums import PostStatus
from .managers import PostManager
from .category import Category
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField
import datetime
import json

class Post(SEOContentMixin, models.Model):
    """ Primary content model with temporal publishing controls """
    objects = PostManager()

    # Core Content fields remain the same
    title = models.CharField(
        max_length=250,
        verbose_name=_("Title"),
        help_text=_("Keep titles under 60 characters for SEO")
    )
    subtitle = models.CharField(
        max_length=250,
        verbose_name=_("Subtitle"),
        blank=True,
        null=True,
        help_text=_("Optional secondary title for social sharing")
    )
    content = RichTextField(
        verbose_name=_("Content"),
        help_text=_("Full post content with rich text formatting")
    )
    
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="posts",
        verbose_name=_("Category"),
        null=True,
        blank=True
    )
    
    slug = models.SlugField(
        max_length=300,
        unique=True,
        unique_for_date="published",
        verbose_name=_("SEO Slug"),
        help_text=_("URL-friendly post identifier")
    )
    
    # Updated temporal fields
    published = models.DateTimeField(
        default=timezone.now,
        verbose_name=_("Publication Date and Time"),
        db_index=True,
        help_text=_("Set publication date and time")
    )
    
    modified = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Last Modified")
    )
    
    status = models.CharField(
        max_length=10,
        choices=PostStatus.choices(),
        default=PostStatus.DRAFT.value,
        verbose_name=_("Post Status"),
        db_index=True
    )
    
    is_pinned = models.BooleanField(
        default=False,
        verbose_name=_("Pinned Post"),
        help_text=_("Feature this post at the top of lists"),
        db_index=True
    )
    
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="authored_posts",
        verbose_name=_("Author")
    )

    class Meta:
        ordering = ["-published", "-is_pinned"]
        verbose_name = _("Blog Post")
        verbose_name_plural = _("Blog Posts")
        indexes = [
            models.Index(fields=["-published", "status"]),
            models.Index(fields=["slug", "status"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["slug", "published"],
                name="unique_post_slug_per_date"
            )
        ]

    def __str__(self) -> str:
        return f"{self.title} ({self.published.strftime('%Y-%m-%d %H:%M')})"

    def clean(self):
        """Validate publication timing"""
        super().clean()
        now = timezone.now()

        if self.status == PostStatus.PUBLISHED.value:
            if self.published > now:
                raise ValidationError(
                    "Cannot publish posts with future dates. Use draft status for scheduling.",
                    code='future_published'
                )

    def save(self, *args, **kwargs):
        """Handle publication timing based on status"""
        now = timezone.now()
        
        # For new posts (no ID) or status changes
        if not self.pk or 'status' in kwargs:
            if self.status == PostStatus.PUBLISHED.value:
                if self.published > now:
                    # Future post - set as draft
                    self.status = PostStatus.DRAFT.value
                else:
                    # Present/past post - set current time
                    self.published = now
        
        super().save(*args, **kwargs)

    @property
    def is_published(self) -> bool:
        """Check if the post is currently published"""
        return (
            self.status == PostStatus.PUBLISHED.value and
            self.published <= timezone.now()
        )

    def publish(self):
        """Publish post and set current timestamp"""
        self.status = PostStatus.PUBLISHED.value
        self.published = timezone.now()
        self.save()

    # Rest of the methods remain the same
    def get_absolute_url(self) -> str:
        return reverse("blog:article", kwargs={'slug': self.slug})

    def get_seo_meta(self) -> dict:
        return {
            "title": self.get_meta_title(),
            "description": self.get_meta_description(),
            "keywords": ", ".join(self.get_keywords_list()),
            "og:type": "article",
            "og:url": self.get_absolute_url(),
            "og:title": self.get_meta_title(),
            "og:description": self.get_meta_description(),
            "og:image": self.get_og_image_url(),
            "twitter:card": "summary_large_image",
            "article:published_time": self.published.isoformat(),
            "article:modified_time": self.modified.isoformat(),
            "article:author": self.author.get_full_name(),
        }

    def get_schema_org_ld_json(self) -> str:
        return json.dumps({
            "@context": "https://schema.org",
            "@type": "BlogPosting",
            "headline": self.title,
            "description": self.get_meta_description(),
            "datePublished": self.published.isoformat(),
            "dateModified": self.modified.isoformat(),
            "author": {
                "@type": "Person",
                "name": self.author.get_full_name(),
                "url": reverse("author-profile", args=[self.author.username])
            },
            "image": self.get_og_image_url(),
            "publisher": {
                "@type": "Organization",
                "name": settings.SITE_NAME,
                "logo": {
                    "@type": "ImageObject",
                    "url": settings.LOGO_URL
                }
            }
        })

    def get_sitemap_entries(self) -> dict:
        return {
            "location": self.get_absolute_url(),
            "lastmod": self.modified,
            "changefreq": "daily",
            "priority": 0.8 if self.is_pinned else 0.5
        }