from rest_framework import serializers

from bookmarks.models import Bookmark

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


class DownloadCreateSerializer(serializers.Serializer):
    """
    Serializer used to start downloads via web frontend.
    """

    bookmark_id = serializers.IntegerField()

    @staticmethod
    def validate_bookmark_id(value):
        """
        Check if bookmark with `bookmark_id` exists in DB.
        Reference: https://www.django-rest-framework.org/api-guide/serializers/#field-level-validation
        """
        bookmark = Bookmark.objects.filter(pk=value).first()
        if not bookmark:
            raise serializers.ValidationError(
                f"Bookmark with bookmark_id={value} does not exist!"
            )
        return value
