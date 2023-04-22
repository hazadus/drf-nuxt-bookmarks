import os
import uuid
from urllib.error import HTTPError

from celery import shared_task
from django.conf import settings
from pytube import YouTube

from .models import Download
from bookmarks.models import Bookmark


@shared_task
def download_bookmark(bookmark_id: int) -> None:
    """
    Add URL to download queue.

    Implement: telegram notification on download completion
    """
    bookmark = Bookmark.objects.get(pk=bookmark_id)
    url = bookmark.url

    if url.startswith("https://www.youtube.com/") or url.startswith(
        "https://youtu.be/" or url.startswith("https://youtube.com/")
    ):
        yt = YouTube(url)
        output_filename = f"{uuid.uuid1()}.mp4"
        output_path = os.path.join(settings.MEDIA_ROOT, "videos")

        if not os.path.exists(output_path):
            os.mkdir(output_path)

        output_full_filename = os.path.join(output_path, output_filename)

        try:
            print("Starting video download from URL: " + url)
            stream = yt.streams.filter(file_extension="mp4")
            stream.get_highest_resolution().download(
                filename=output_full_filename,
            )

            file_stats = os.stat(output_full_filename)

            print(f"Video saved to file {output_filename}")
            print(f"File Size in Bytes is {file_stats.st_size}")

            download = Download()
            download.title = yt.title
            download.status = Download.Status.COMPLETED
            download.bookmark = bookmark
            download.file.name = "/videos/{filename}".format(
                filename=output_filename,
            )
            download.file_size = file_stats.st_size
            download.save()
        except HTTPError as e:
            print(f"An error has occured while downloading video: {e.info}")
            return
