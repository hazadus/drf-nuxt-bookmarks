from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _


class Folder(models.Model):
    """
    Represents user-created folder with bookmarks.
    """

    user = models.ForeignKey(
        verbose_name=_("user"),
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name="folders",
    )
    title = models.CharField(
        verbose_name=_("title"),
        max_length=64,
    )

    class Meta:
        ordering = ["title"]
        verbose_name = _("folder")
        verbose_name_plural = _("folders")

    def __str__(self):
        return self.title


class Bookmark(models.Model):
    """
    Represents user-created site bookmark.
    """

    user = models.ForeignKey(
        verbose_name=_("user"),
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name="bookmarks",
    )
    url = models.URLField(verbose_name=_("URL"))
    title = models.CharField(
        verbose_name=_("title"),
        max_length=64,
    )
    description = models.TextField(
        verbose_name=_("description"),
        blank=True,
        null=True,
    )
    image_url = models.URLField(
        verbose_name=_("image URL"),
        blank=True,
        null=True,
    )
    folder = models.ForeignKey(
        verbose_name=_("folder"),
        to=Folder,
        on_delete=models.CASCADE,
        related_name="bookmarks",
        blank=True,
        null=True,
        default=None,
    )
    is_favorite = models.BooleanField(
        verbose_name=_("favorite"),
        default=False,
    )
    is_archived = models.BooleanField(
        verbose_name=_("archived"),
        default=False,
    )
    created = models.DateTimeField(verbose_name=_("created"), auto_now_add=True)
    updated = models.DateTimeField(verbose_name=_("updated"), auto_now=True)

    class Meta:
        ordering = ["-created"]
        verbose_name = _("bookmark")
        verbose_name_plural = _("bookmarks")

    def __str__(self):
        return self.title
