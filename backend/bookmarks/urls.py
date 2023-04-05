from django.urls import path

from .views import BookmarksListView, bookmark_create_from_telegram

urlpatterns = [
    path("bookmarks/", BookmarksListView.as_view()),
    path("bookmarks/create_from_telegram/", bookmark_create_from_telegram),
]
