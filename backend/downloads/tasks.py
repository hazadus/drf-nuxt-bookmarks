import os
import uuid

from celery import shared_task
from django.conf import settings
from pytube import YouTube

from .models import Download


@shared_task
def process_download(download_id: int) -> None:  # noqa: max-complexity: 4
    """
    Process Download instance with `download_id` depending on it's status and type.

    Depending on status, this task:
    - "pending": do the download;
    - "completed": do nothing and return;
    - "failed": change status to "pending", then retry downloading.

    Bookmark's URL is checked: if it points to YouTube, then we try to download it.
    Other sites are not supported for now: Download instance gets deleted .
    """
    download = Download.objects.get(pk=download_id)

    if download.status == Download.Status.COMPLETED:
        return
    elif download.status == Download.Status.FAILED:
        download.status = Download.Status.PENDING
        download.save()

    if is_youtube_link(url=download.bookmark.url):
        download_from_youtube(download=download)
    else:
        download.delete()


def is_youtube_link(url: str) -> bool:
    """
    Return True if `url` is a link to YouTube.
    """
    return url.startswith("https://www.youtube.com/") or url.startswith(
        "https://youtu.be/" or url.startswith("https://youtube.com/")
    )


def download_from_youtube(download: Download) -> None:  # noqa: max-complexity: 4
    """
    Download video from YouTube and save it to file.
    """
    url = download.bookmark.url
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

        download.title = yt.title
        download.status = Download.Status.COMPLETED
        download.file.name = "videos/{filename}".format(
            filename=output_filename,
        )
        download.file_size = file_stats.st_size
    except Exception as e:
        print(f"An error has occured while downloading video: {e}")
        download.status = Download.Status.FAILED
    finally:
        download.save()
