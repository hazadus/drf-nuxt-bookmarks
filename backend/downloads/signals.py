from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import Download


@receiver(post_delete, sender=Download)
def delete_attached_file(sender, instance, **kwargs):
    """
    Delete attached file when model instance gets deleted without explicit call of `Download.delete()`.

    Issue: https://code.djangoproject.com/ticket/12034
    Reference: https://docs.djangoproject.com/en/4.0/ref/signals/#post-delete
    """
    if instance.file:
        instance.file.delete(save=False)
