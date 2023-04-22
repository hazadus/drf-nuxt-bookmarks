from rest_framework import serializers

from .models import Download


class DownloadSerializer(serializers.ModelSerializer):
    """
    Serializer for Download model.
    """

    class Meta:
        model = Download
        fields = [
            "id",
            "title",
            "status",
            "file",
            "file_size",
            "created",
            "updated",
        ]
