from django.contrib import admin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from ..models import Post, PostStatus

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Admin interface for Post model with strong typing 📜"""

    list_display = ('title', 'slug', 'published', 'is_published')
    list_filter = ("status", "published", "category")
    search_fields = ("title", "content", "category__name")

    prepopulated_fields = {"slug": ("title",)}
    
    # Make 'is_published' read-only in the admin
    readonly_fields = ("is_published",)
    actions = ["publish_selected", "unpublish_selected", "schedule_for_future"]
    
    # Organize fields into sections
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'subtitle', 'author', 'category', 'content')
        }),
        ('Publication', {
            'fields': ('published', 'status', 'is_pinned', 'is_published'),
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description', 'keywords', 'og_image', 'canonical_url'),
            'classes': ('collapse',)
        }),
    )

    def is_published(self, obj: Post) -> str:
        """Display published status with a colored badge"""
        if obj.is_published:
            return format_html('<span style="color: green;">✔ Published</span>')
        return format_html('<span style="color: red;">✘ Not Published</span>')
    is_published.short_description = _("Published Status")

    def publish_selected(self, request, queryset):
        """Admin action to publish selected posts"""
        updated = queryset.update(
            status=PostStatus.PUBLISHED.value,
            published=timezone.now()
        )
        self.message_user(request, _(f"{updated} posts were successfully published."))
    publish_selected.short_description = _("Publish selected posts")

    def unpublish_selected(self, request, queryset):
        """Admin action to unpublish selected posts"""
        updated = queryset.update(status=PostStatus.DRAFT.value)
        self.message_user(request, _(f"{updated} posts were unpublished."))
    unpublish_selected.short_description = _("Unpublish selected posts")

    def schedule_for_future(self, request, queryset):
        """Admin action to schedule posts for future publishing"""
        for post in queryset:
            if post.status == PostStatus.PUBLISHED.value:
                post.status = PostStatus.DRAFT.value
                post.save()
        self.message_user(request, _("Selected posts were scheduled for future publishing."))
    schedule_for_future.short_description = _("Schedule for future publishing")

    def save_model(self, request, obj: Post, form, change):
        """Handle past-date confirmation and scheduled publishing"""
        if obj.published < timezone.now() and not request.POST.get("allow_past_date"):
            raise ValidationError(
                _("You're setting a past date. Check the 'Allow Past Date' box to confirm.")
            )
        
        if obj.published > timezone.now() and obj.status == PostStatus.PUBLISHED.value:
            obj.status = PostStatus.DRAFT.value
            self.message_user(
                request,
                _("Post scheduled for future publishing. Status set to 'Draft'."),
                level="warning"
            )
        
        super().save_model(request, obj, form, change)