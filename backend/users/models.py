from django.contrib.auth.models import AbstractUser
from django.db import models
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

    def __str__(self):
        return self.username
