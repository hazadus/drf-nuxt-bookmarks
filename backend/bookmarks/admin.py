from django.contrib import admin

from .models import Bookmark, Folder, Tag


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


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    Configures admin panel views for Tags.
    """

    model = Tag
    list_display = [
        "title",
    ]
    ordering = ["title"]


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
        "is_read",
        "is_archived",
        "created",
    ]
    list_filter = ["is_archived", "is_favorite", "is_read"]
    search_fields = ["title"]
    ordering = ["user", "is_archived", "-is_favorite", "is_read", "-created"]
