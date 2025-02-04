from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    """📂 Content taxonomy system with automatic slug generation"""

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=50, unique=True, verbose_name=_("Category Name"))
    slug = models.SlugField(max_length=60, unique=True, verbose_name=_("Category Slug"))
    description = models.TextField(blank=True, verbose_name=_("Category Description"))

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("blog:category", kwargs={"slug": self.slug})

    def get_seo_meta(self):
        """Generate category-specific SEO metadata"""
        return {
            "title": self.get_meta_title() or f"Posts in {self.name}",
            "description": self.get_meta_description() or self.description,
            "og:type": "website",
            "og:url": self.get_absolute_url(),
        }
