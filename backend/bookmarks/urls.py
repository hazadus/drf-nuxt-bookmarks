from django.urls import path

from .views import (
    TagListView,
    FolderListView,
    BookmarkListView,
    bookmark_create_from_telegram,
    bookmark_create_from_web,
    BookmarkUpdateView,
)

urlpatterns = [
    path("tags/", TagListView.as_view()),
    path("folders/", FolderListView.as_view()),
    path("bookmarks/", BookmarkListView.as_view()),
    path("bookmarks/create_from_telegram/", bookmark_create_from_telegram),
    path("bookmarks/create/", bookmark_create_from_web),
    path("bookmarks/update/<int:pk>/", BookmarkUpdateView.as_view()),
]
