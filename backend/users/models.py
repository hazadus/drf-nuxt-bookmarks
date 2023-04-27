from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    """
    Custom user model with additional fields.
    """

    telegram_id = models.CharField(
        verbose_name=_("telegram id"), max_length=32, blank=True, null=True
    )
    profile_image = models.ImageField(
        verbose_name=_("profile image"), null=True, blank=True, upload_to="images/"
    )
    disk_quota = models.IntegerField(
        verbose_name=_("disk quota, Mb"),
        default=0,
    )

    def __str__(self):
        return self.username

    @property
    def disk_space_used(self):
        """
        Return disk space (in Mb) used by user's downloads.
        """
        from downloads.models import Download

        downloads = Download.objects.filter(bookmark__user_id=self.id)
        disk_space_used = downloads.aggregate(disk_space_used=Sum("file_size")).get(
            "disk_space_used"
        )
        return round(disk_space_used / (1024 * 1024), 1) if disk_space_used else 0
