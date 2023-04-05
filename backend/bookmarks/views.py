from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Bookmark
from .serializers import BookmarkCreateFromTelegramSerializer, BookmarkListSerializer
from .utils import parse_url_info


class BookmarksListView(APIView):
    """
    List all bookmarks.
    """

    @staticmethod
    def get(request: Request) -> Response:
        """
        Return all bookmarks.
        """
        bookmarks = Bookmark.objects.all()
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
