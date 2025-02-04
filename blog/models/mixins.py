from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class SEOContentMixin(models.Model):
    """ Search Engine Optimization foundation for content models """
    meta_title = models.CharField(
        max_length=60,
        verbose_name= _("Meta Title"),
        blank=True,
        help_text= _("60 characters max. Important for SEO and social sharing")
    )
    meta_description = models.TextField(
        max_length=160,
        verbose_name= _("Meta Description"),
        blank=True,
        help_text= _("160 characters max. Summarize content for search engines")
    )
    keywords = models.TextField(
        verbose_name= _("Keywords"),
        blank=True,
        help_text= _("Comma-separated list of SEO keywords (max 10)")
    )
    og_image = models.ImageField(
        upload_to="og_images/",
        verbose_name= _("Open Graph Image"),
        blank=True,
        help_text= _("1200x630 pixels (1.91:1 ratio) for social sharing")
    )
    canonical_url = models.URLField(
        verbose_name=_("Canonical URL"),
        blank=True,
        help_text= _("Set if this content exists elsewhere")
    )

    class Meta:
        abstract = True

    def get_meta_title(self):
        return self.meta_title or self.title
    
    def get_meta_description(self):
        return self.meta_description or self.content[:160].strip() + "..."

    def get_keywords_list(self):
        return [k.strip().lower() for k in self.keywords.split(",") if k.strip()][:10]

    def get_og_image_url(self):
        if self.og_image:
            return self.og_image.url
        return settings.DEFAULT_OG_IMAGE_URL

    class Meta:
        abstract = True