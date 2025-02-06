from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.generic.base import TemplateView, RedirectView

from . import views
from . import api

app_name: str = "blog"


urlpatterns: list[path] = [
    # 🏠 Homepage route
    path("", views.HomeView.as_view(), name="home"),
    # ℹ️ About page with trailing slash best practice
    path("about-me", views.AboutView.as_view(), name="about"),
    # 📖 Post detail with slug parameter (more secure than PK!)
    path("<slug:slug>/", views.PostView.as_view(), name="article"),
    # 🔗 Static pages
    path(
        "connect-me",
        TemplateView.as_view(template_name="pages/connect.html"),
        name="connect_me",
    ),
    path("terms", TemplateView.as_view(template_name="pages/terms.html"), name="terms"),
    path(
        "security",
        TemplateView.as_view(template_name="pages/security.html"),
        name="security",
    ),
    path(
        "privacy",
        TemplateView.as_view(template_name="pages/privacy.html"),
        name="privacy",
    ),
    path(
        "support",
        TemplateView.as_view(template_name="pages/support.html"),
        name="support",
    ),
    # path('category/<slug:slug>/', views.category_detail, name='category'),
    path('api/update-history/', api.get_update_history, name='update_history'),
]


# 🔧 Development-only static files (auto-disabled when DEBUG=False)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
