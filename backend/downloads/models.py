from django.db import models
from django.utils.translation import gettext_lazy as _

from bookmarks.models import Bookmark


class Download(models.Model):
    """
    Represents content downloaded from Bookmark's url, packed in one file.
    """

    class Status(models.TextChoices):
        PENDING = "PG", _("Pending")
        COMPLETED = "CD", _("Completed")
        FAILED = "FD", _("Failed")

    title = models.CharField(verbose_name=_("title"), max_length=512)
    status = models.CharField(
        verbose_name=_("status"),
        max_length=2,
        choices=Status.choices,
        default=Status.PENDING,
    )
    bookmark = models.ForeignKey(
        verbose_name=_("bookmark"),
        to=Bookmark,
        on_delete=models.CASCADE,
        related_name="downloads",
        blank=True,
        null=True,
        default=None,
    )
    file = models.FileField(verbose_name=_("file"))
    file_size = models.IntegerField(verbose_name=_("file size, bytes"))
    created = models.DateTimeField(verbose_name=_("created"), auto_now_add=True)
    updated = models.DateTimeField(verbose_name=_("updated"), auto_now=True)

    class Meta:
        verbose_name = _("download")
        verbose_name_plural = _("downloads")
        ordering = ["-created"]

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        """
        Delete file with Download instance.
        """
        self.file.delete(save=False)
        super().delete(*args, **kwargs)
