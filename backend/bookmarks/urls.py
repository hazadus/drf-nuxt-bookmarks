from django.urls import path

from .views import (
    BookmarkDeleteView,
    BookmarkListView,
    BookmarkUpdateView,
    FolderDeleteView,
    FolderListView,
    FolderUpdateView,
    TagListView,
    bookmark_create_from_telegram,
    bookmark_create_from_web,
    folder_create,
)

urlpatterns = [
    path("tags/", TagListView.as_view()),
    path("folders/", FolderListView.as_view()),
    path("folders/create/", folder_create),
    path("folders/update/<int:pk>/", FolderUpdateView.as_view()),
    path("folders/delete/<int:pk>/", FolderDeleteView.as_view()),
    path("bookmarks/", BookmarkListView.as_view()),
    path("bookmarks/create_from_telegram/", bookmark_create_from_telegram),
    path("bookmarks/create/", bookmark_create_from_web),
    path("bookmarks/update/<int:pk>/", BookmarkUpdateView.as_view()),
    path("bookmarks/delete/<int:pk>/", BookmarkDeleteView.as_view()),
]
