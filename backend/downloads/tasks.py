import os
import uuid

from celery import shared_task
from django.conf import settings
from pytube import YouTube

from .models import Download


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=2,
    retry_jitter=True,
    retry_kwargs={
        "max_retries": 5,
    },
)
def process_download(self, download_id: int) -> None:  # noqa: max-complexity: 5
    """
    Process Download instance with `download_id` depending on it's status and type.

    Depending on status, this task:
    - "pending": do the download;
    - "completed": do nothing and return;
    - "failed": change status to "pending", then retry downloading.

    Bookmark's URL is checked: if it points to YouTube, then we try to download the video.
    Other sites are not supported for now: Download instance gets deleted.

    There's a bug in pytube causing video sometimes not get downloaded on the first try,
    so we have to make some retries. Issue: https://github.com/pytube/pytube/issues/1542
    """
    download = Download.objects.get(pk=download_id)

    if not is_youtube_link(url=download.bookmark.url):
        download.delete()
        return

    if download.status == Download.Status.COMPLETED:
        return
    elif download.status == Download.Status.FAILED:
        download.status = Download.Status.PENDING
        download.save()

    if not download_from_youtube(download=download):
        raise Exception()


def is_youtube_link(url: str) -> bool:
    """
    Return True if `url` is a link to YouTube.
    """
    return url.startswith("https://www.youtube.com/") or url.startswith(
        "https://youtu.be/" or url.startswith("https://youtube.com/")
    )


def download_from_youtube(download: Download) -> bool:  # noqa: max-complexity: 4
    """
    Download YouTube video from `download.bookmark.url` and save it to a file in "MEDIA_ROOT/videos" folder.
    Save title, file name, file size, download status to the `download` instance.
    Return True if succeeded, otherwise False.
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
        return True if download.status is Download.Status.COMPLETED else False
