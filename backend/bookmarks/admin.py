from django.contrib import admin

from .models import Bookmark, Folder


@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):
    """
    Configures admin panel views for Folders.
    """

    model = Folder
    list_display = [
        "title",
        "user",
    ]
    ordering = ["user", "title"]


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    """
    Configures admin panel views for Bookmarks.
    """

    model = Bookmark
    list_display = [
        "title",
        "user",
        "folder",
        "is_favorite",
        "is_archived",
        "created",
    ]
    ordering = ["-created"]
