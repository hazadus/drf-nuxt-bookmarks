from rest_framework import serializers

from users.models import CustomUser
from users.serializers import CustomUserTelegramIDSerializer

from .models import Bookmark, Folder, Tag


class FolderSerializer(serializers.ModelSerializer):
    """
    Serializer for Folder model.
    """

    class Meta:
        model = Folder
        fields = [
            "id",
            "user",
            "title",
        ]


class TagSerializer(serializers.ModelSerializer):
    """
    Serializer for Tag model.
    """

    class Meta:
        model = Tag
        fields = [
            "id",
            "title",
        ]


class BookmarkListSerializer(serializers.ModelSerializer):
    """
    Serializer for Bookmark model - for list view.
    """

    folder = FolderSerializer(many=False)
    tags = TagSerializer(many=True)

    class Meta:
        model = Bookmark
        fields = [
            "id",
            "user",
            "url",
            "title",
            "description",
            "image_url",
            "folder",
            "tags",
            "is_favorite",
            "is_read",
            "is_archived",
            "created",
            "updated",
        ]


class BookmarkCreateFromTelegramSerializer(serializers.ModelSerializer):
    """
    Serializer for Bookmark model - for creating new bookmarks.
    """

    user = CustomUserTelegramIDSerializer(many=False)

    class Meta:
        model = Bookmark
        fields = [
            "user",
            "url",
        ]

    def create(self, validated_data):
        """
        Create new bookmark with `user` identified by `telegram_id`.
        Reference: https://www.django-rest-framework.org/api-guide/relations/#writable-nested-serializers
        """
        telegram_id = validated_data.pop("user").get("telegram_id")
        # NB: we checked existence of user with `telegram_id` in `CustomUserTelegramIDSerializer.validate_telegram_id()`
        user = CustomUser.objects.filter(telegram_id=telegram_id).first()
        bookmark = Bookmark.objects.create(user=user, **validated_data)
        return bookmark
