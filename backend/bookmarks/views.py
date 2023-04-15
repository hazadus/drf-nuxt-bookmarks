from django.db.models import Count, Q
from rest_framework import authentication, permissions, status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.generics import UpdateAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Bookmark, Folder, Tag
from .serializers import (
    BookmarkCreateFromTelegramSerializer,
    BookmarkCreateFromWebSerializer,
    BookmarkListSerializer,
    BookmarkUpdateSerializer,
    FolderListSerializer,
    TagListSerializer,
)
from .utils import parse_url_info


class TagListView(APIView):
    """
    List all Tags applied to user's bookmarks.
    """

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def get(request: Request) -> Response:
        """
        Return all Tags applied to user's bookmarks.
        Tags are annotated with `bookmarks_qty` - count of user's bookmarks marked with each tag.
        """
        tags = (
            Tag.objects.filter(
                bookmarks__user_id__exact=request.user.pk,
            )
            .annotate(
                bookmarks_qty=Count(
                    "bookmarks",
                    filter=Q(
                        bookmarks__user_id__exact=request.user.pk,
                    ),
                ),
            )
            .order_by("title")
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
        Folders are annotated with `bookmarks_qty` - count of bookmarks in each folder.
        """
        folders = (
            Folder.objects.filter(user_id__exact=request.user.pk)
            .annotate(
                bookmarks_qty=Count(
                    "bookmarks",
                    filter=Q(
                        bookmarks__user_id__exact=request.user.pk,
                    )
                    & Q(
                        bookmarks__is_archived=False,
                    ),
                ),
            )
            .order_by("title")
        )
        serializer = FolderListSerializer(folders, many=True)
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


@api_view(["POST"])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def bookmark_create_from_web(request: Request) -> Response:
    """
    Create new bookmark. Assign to authenticated user.

    Post data example:
    {
        "url": "https://ru.vuejs.org/v2/cookbook/dockerize-vuejs-app.html"
    }
    """
    serializer = BookmarkCreateFromWebSerializer(data=request.data)

    if serializer.is_valid():
        bookmark = serializer.save()

        title, description, image_url = parse_url_info(serializer.data.get("url"))
        bookmark.title = title
        bookmark.description = description
        bookmark.image_url = image_url
        bookmark.user = request.user
        bookmark.save()

        # Return detailed bookmark info to the user:
        detail_serializer = BookmarkListSerializer(instance=bookmark, many=False)
        return Response(detail_serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookmarkUpdateView(UpdateAPIView):
    """
    Partially update bookmark data. Return updated data.
    """

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    queryset = Bookmark.objects.all()
    serializer_class = BookmarkUpdateSerializer

    # def put(self, request, *args, **kwargs):
    #     """
    #     PATCH method must be used to partially update bookmark data.
    #     Return updated data.
    #     """
    #     return self.partial_update(request, *args, **kwargs)
