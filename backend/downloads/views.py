from rest_framework import authentication, permissions, status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.request import Request
from rest_framework.response import Response

from downloads.tasks import download_bookmark

from .serializers import DownloadCreateSerializer


@api_view(["POST"])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def download_start_from_web(request: Request) -> Response:
    """
    Start download for bookmark's URL. Assign it to the bookmark.

    Post data example:
    {
        "bookmark_id": 1
    }
    """
    serializer = DownloadCreateSerializer(data=request.data)

    if serializer.is_valid():
        download_bookmark.delay(bookmark_id=serializer.data.get("bookmark_id"))
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
