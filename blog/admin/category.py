from django.contrib import admin
from django.db import models
from django.urls import reverse
from django.utils.html import format_html
from ..models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin interface for blog post categories"""

    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "slug", "post_count", "description_short", "category_links")
    search_fields = ("name", "description")
    list_filter = ("created", "modified")
    readonly_fields = ("post_count",)
    date_hierarchy = "created"
    list_per_page = 25

    fieldsets = (
        (None, {"fields": ("name", "slug", "description")}),
        ("Statistics", {"fields": ("post_count",), "classes": ("collapse",)}),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(_post_count=models.Count("posts"))

    def post_count(self, obj):
        url = reverse("admin:blog_post_changelist") + f"?category__id__exact={obj.id}"
        return format_html('<a href="{}">{}</a>', url, obj._post_count)

    post_count.short_description = "Posts"
    post_count.admin_order_field = "_post_count"

    def description_short(self, obj):
        return obj.description[:75] + "..." if obj.description else ""

    description_short.short_description = "Description"

    def category_links(self, obj):
        try:
            url = obj.get_absolute_url()
            return format_html('<a href="{}" target="_blank">View Live</a>', url)
        except:
            return "URL not configured"

    category_links.short_description = "Actions"
