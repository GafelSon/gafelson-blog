from django.contrib import admin
from django.urls import include, path
from django.views.decorators.cache import cache_page
from django.conf import settings
from django.conf.urls import handler404, handler500

# Type hints for better IDE support
from django.urls.resolvers import URLPattern, URLResolver
from typing import List, Union

from blog.views import NotFoundView, ServerErrorView
from django_ckeditor_5.views import upload_file

urlpatterns: List[Union[URLPattern, URLResolver]] = [
    # Admin panel with security through obscurity
    path(f"{settings.ADMIN_URL}", admin.site.urls),
    # Blog routes with caching in production
    path("", include(("blog.urls", "blog"), namespace="blog")),
    path("", cache_page(500)(include("blog.urls")), name="cached_home"),
    # Security endpoints
    path("security/", include("django.contrib.auth.urls")),
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
