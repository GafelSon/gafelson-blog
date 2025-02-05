from django.contrib import admin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from ..models import Post, PostStatus

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Admin interface for Post model with temporal publishing controls"""

    list_display = ('title', 'slug', 'published', 'is_published')
    list_filter = ("status", "published", "category")
    search_fields = ("title", "content", "category__name")

    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("is_published",)
    actions = ["publish_selected", "unpublish_selected", "schedule_for_future"]
    
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
        """Admin action to publish selected posts immediately"""
        now = timezone.now()
        updated = 0
        
        for post in queryset:
            post.status = PostStatus.PUBLISHED.value
            post.published = now
            post.save()
            updated += 1
            
        self.message_user(request, _(f"{updated} posts were successfully published."))
    publish_selected.short_description = _("Publish selected posts")

    def unpublish_selected(self, request, queryset):
        """Admin action to unpublish selected posts"""
        updated = queryset.update(status=PostStatus.DRAFT.value)
        self.message_user(request, _(f"{updated} posts were unpublished."))
    unpublish_selected.short_description = _("Unpublish selected posts")

    def schedule_for_future(self, request, queryset):
        """Admin action to ensure posts are drafts for future publishing"""
        now = timezone.now()
        updated = 0
        
        for post in queryset:
            if post.published > now:
                post.status = PostStatus.DRAFT.value
                post.save()
                updated += 1
                
        self.message_user(request, _(f"{updated} posts were scheduled for future publishing."))
    schedule_for_future.short_description = _("Schedule for future publishing")

    def get_queryset(self, request):
        """Get queryset for admin view"""
        return super().get_queryset(request)

    def save_model(self, request, obj: Post, form, change):
        """Handle publication timing and status"""
        now = timezone.now()
        
        if obj.status == PostStatus.PUBLISHED.value:
            if obj.published > now:
                # Future posts must be drafts
                obj.status = PostStatus.DRAFT.value
                self.message_user(
                    request,
                    _("Future posts must be drafts. Status has been updated."),
                    level="warning"
                )
            else:
                # Present/past posts get current timestamp
                obj.published = now
                self.message_user(
                    request,
                    _("Post published with current timestamp."),
                    level="info"
                )
        
        super().save_model(request, obj, form, change)