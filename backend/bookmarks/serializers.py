from rest_framework import serializers

from users.models import CustomUser
from users.serializers import CustomUserTelegramIDSerializer

from .models import Bookmark, Folder, Tag


class FolderSerializer(serializers.ModelSerializer):
    """
    Serializer for Folder model.
    """

    # NB: this is to get `id` field in nested serializers - we need it in `BookmarkUpdateSerializer.update()`
    id = serializers.IntegerField(read_only=False)

    class Meta:
        model = Folder
        fields = [
            "id",
            "user",
            "title",
        ]


class FolderListSerializer(serializers.ModelSerializer):
    """
    Serializer for Folder model with `bookmarks_qty` field - count of bookmarks in each folder.
    """

    bookmarks_qty = serializers.IntegerField()

    class Meta:
        model = Folder
        fields = [
            "id",
            "user",
            "title",
            "bookmarks_qty",
        ]


class TagSerializer(serializers.ModelSerializer):
    """
    Serializer for Tag model.
    """

    # NB: this is to get `id` field in nested serializers - we need it in `BookmarkUpdateSerializer.update()`
    id = serializers.IntegerField(read_only=False)

    class Meta:
        model = Tag
        fields = [
            "id",
            "title",
        ]


class TagListSerializer(serializers.ModelSerializer):
    """
    Serializer for Tag model with `bookmarks_qty` field - count of bookmarks with each tag.
    """

    bookmarks_qty = serializers.IntegerField()

    class Meta:
        model = Tag
        fields = [
            "id",
            "title",
            "bookmarks_qty",
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


class BookmarkUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for Bookmark - for updating bookmarks via frontend.
    Note: we dont mess with tags yet...
    """

    folder = FolderSerializer(many=False)
    tags = TagSerializer(many=True)

    class Meta:
        model = Bookmark
        fields = [
            "url",
            "title",
            "description",
            "image_url",
            "folder",
            "tags",
            "is_favorite",
            "is_read",
            "is_archived",
        ]

    def update(self, instance, validated_data):
        """
        Override `update` to deal with nested objects.
        """
        instance.url = validated_data.get("url")
        instance.title = validated_data.get("title")
        instance.description = validated_data.get("description")
        instance.image_url = validated_data.get("image_url")
        instance.is_favorite = validated_data.get("is_favorite")
        instance.is_read = validated_data.get("is_read")
        instance.is_archived = validated_data.get("is_archived")

        # Take care of nested objects
        if folder_data := validated_data.get("folder"):
            if folder_id := folder_data.get("id"):
                instance.folder = Folder.objects.get(pk=folder_id)
        else:
            instance.folder = None

        # Remove all tag relations
        instance.tags.clear()

        if tags := validated_data.get("tags"):
            for tag_data in tags:
                tag = Tag.objects.filter(id=tag_data.get("id")).first()
                if tag not in instance.tags.all():
                    instance.tags.add(tag)

        instance.save()
        return instance
