from django.apps import AppConfig


class DownloadsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "downloads"

    def ready(self):
        try:
            import downloads.signals  # noqa: F401
        except ImportError:
            pass
