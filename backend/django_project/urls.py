"""django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.utils.translation import gettext_lazy as _

urlpatterns = [
    path("admin/", admin.site.urls),
    # Local apps
    path("api/v1/", include("bookmarks.urls")),
    path("api/v1/", include("users.urls")),
    path("api/v1/", include("downloads.urls")),
    # Djoser endpoints to manage users:
    path("api/v1/", include("djoser.urls")),
    path("api/v1/", include("djoser.urls.authtoken")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Configure Admin panel titles
admin.site.site_header = _("Bookmarks Administration Dashboard")
admin.site.site_title = _("Bookmarks Administration")
admin.site.index_title = _("Bookmarks Administration")
