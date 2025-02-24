from django.contrib import admin
from django.urls import include, path
from django.views.decorators.cache import cache_page
from django.conf import settings
from django.conf.urls import handler404, handler500
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import GenericSitemap
from django.utils.functional import lazy
from blog.models import Post, Category

# Type hints for better IDE support
from django.urls.resolvers import URLPattern, URLResolver
from typing import List, Union

from blog.views import NotFoundView, ServerErrorView

# Sitemap configuration
def get_sitemaps():
    return {
        'posts': GenericSitemap({
            'queryset': Post.objects.filter(status='published'),
            'date_field': 'modified',
        }, priority=0.9),
        'categories': GenericSitemap({
            'queryset': Category.objects.all(),
            'date_field': 'modified',
        }, priority=0.8),
    }

sitemaps = lazy(get_sitemaps, dict)()

urlpatterns: List[Union[URLPattern, URLResolver]] = [
    # Admin panel
    path(f"{settings.ADMIN_URL}/", admin.site.urls),
    # Blog routes with namespace for API and other named URLs
    path("", include(("blog.urls", "blog"), namespace="blog")),
    # Cached routes for performance
    path("", cache_page(500)(include("blog.urls"))),
    # Security endpoints
    path("security/", include("django.contrib.auth.urls")),
    # Sitemap endpoints
    # path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    # path('robots.txt', include('robots.urls')),
]

# Error handlers for production
handler404 = NotFoundView.as_view()
handler500 = ServerErrorView.as_view()

# Development-only routes
if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
