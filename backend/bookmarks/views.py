from django.db.models import Count
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import authentication, permissions

from .models import Bookmark, Tag, Folder
from .serializers import (
    BookmarkCreateFromTelegramSerializer,
    BookmarkListSerializer,
    TagListSerializer,
    FolderSerializer,
)
from .utils import parse_url_info


class TagListView(APIView):
    """
    List all Tags.
    """

    @staticmethod
    def get(request: Request) -> Response:
        """
        Return all Tags.
        """
        tags = Tag.objects.all().annotate(
            bookmarks_qty=Count("bookmarks"),
        )
        serializer = TagListSerializer(tags, many=True)
        return Response(serializer.data)


class FolderListView(APIView):
    """
    List all user's Folders.
    """

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def get(request: Request) -> Response:
        """
        Return all user's Folders.
        """
        folders = Folder.objects.filter(user_id__exact=request.user.pk)
        serializer = FolderSerializer(folders, many=True)
        return Response(serializer.data)


class BookmarkListView(APIView):
    """
    List all user's bookmarks.
    """

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def get(request: Request) -> Response:
        """
        Return all user's bookmarks.
        """
        bookmarks = Bookmark.objects.filter(user_id__exact=request.user.pk)
        serializer = BookmarkListSerializer(bookmarks, many=True)
        return Response(serializer.data)


@api_view(["POST"])
def bookmark_create_from_telegram(request: Request) -> Response:
    """
    Create new bookmark. Assign to user with "telegram_id" (if exists).

    Post data example:
    {
        "user": {
            "telegram_id": "133637887"
        },
        "url": "https://ru.vuejs.org/v2/cookbook/dockerize-vuejs-app.html"
    }
    """
    serializer = BookmarkCreateFromTelegramSerializer(data=request.data)

    if serializer.is_valid():
        # NB: we check existence of user with `telegram_id` in `CustomUserTelegramIDSerializer.validate_telegram_id()`
        bookmark = serializer.save()

        title, description, image_url = parse_url_info(serializer.data.get("url"))
        bookmark.title = title
        bookmark.description = description
        bookmark.image_url = image_url
        bookmark.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
