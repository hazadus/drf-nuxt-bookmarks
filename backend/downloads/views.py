from rest_framework import authentication, permissions, status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.request import Request
from rest_framework.response import Response

from bookmarks.models import Bookmark
from downloads.models import Download
from downloads.tasks import process_download

from .serializers import DownloadCreateSerializer, DownloadSerializer


@api_view(["POST"])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def download_start_from_web(request: Request) -> Response:  # noqa: max-complexity: 4
    """
    Check if there's already a download instance for passed bookmark.
    Then either:
    - create new Download instance with `pending` status, with `bookmark` field set to bookmark with posted id.
    - pass existing Download to Celery task.
    Run Celery `process_download` task, with `id` of the Download instance.
    Return the Download instance, serialized to JSON.

    Post data example:
    {
        "bookmark_id": 1
    }
    """
    serializer = DownloadCreateSerializer(data=request.data)

    if serializer.is_valid():
        bookmark = Bookmark.objects.get(
            pk=serializer.data.get("bookmark_id"),
        )

        if hasattr(bookmark, "download"):
            download = bookmark.download
            if download.status == Download.Status.FAILED:
                download.status = Download.Status.PENDING
                download.save()
        else:
            download = Download()
            download.title = bookmark.title
            download.bookmark = bookmark
            download.save()

        process_download.delay(download_id=download.pk)

        return Response(
            DownloadSerializer(instance=download).data,
            status=status.HTTP_201_CREATED,
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
