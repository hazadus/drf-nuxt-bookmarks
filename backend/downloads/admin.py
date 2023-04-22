from django.contrib import admin

from .models import Download


@admin.register(Download)
class DownloadAdmin(admin.ModelAdmin):
    """
    Configures admin panel views for Downloads.
    """

    model = Download
    list_display = [
        "title",
        "status",
        "file_size",
        "created",
    ]
    list_filter = ["status"]
    ordering = ["-created"]
