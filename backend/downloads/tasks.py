import uuid
from urllib.error import HTTPError

from celery import shared_task
from pytube import YouTube


@shared_task
def download_url(url: str) -> None:
    """
    Add URL to download queue.

    Implement: telegram notification on download completion
    Implement: save to /media/videos/ dir
    """
    if url.startswith("https://www.youtube.com/") or url.startswith(
        "https://youtu.be/"
    ):
        yt = YouTube(url)
        output_filename = f"{uuid.uuid1()}.mp4"

        try:
            print("Starting video download from URL: " + url)
            stream = yt.streams.filter(file_extension="mp4")
            stream.get_highest_resolution().download(filename=output_filename)
            print(f"Video saved to file {output_filename}")
        except HTTPError as e:
            print(f"An error has occured while downloading video: {e.info}")
            return
