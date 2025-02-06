from django.contrib import admin
from ..models import UpdateVersion, UpdateFeature, UpdateBugFix

class UpdateFeatureInline(admin.TabularInline):
    model = UpdateFeature
    extra = 1

class UpdateBugFixInline(admin.TabularInline):
    model = UpdateBugFix
    extra = 1

@admin.register(UpdateVersion)
class UpdateVersionAdmin(admin.ModelAdmin):
    list_display = ('version', 'date')
    list_filter = ('date',)
    search_fields = ('version',)
    ordering = ('-date', '-version')
    inlines = [UpdateFeatureInline, UpdateBugFixInline]
    
    fieldsets = (
        (None, {
            'fields': ('version', 'date')
        }),
    )