from rest_framework import serializers

from .models import CustomUser


class CustomUserTelegramIDSerializer(serializers.ModelSerializer):
    """
    Serializer for CustomUser model with only "telegram_id" field.
    Used to identify user by telegram_id when creating new Bookmarks.
    """

    class Meta:
        model = CustomUser
        fields = [
            "telegram_id",
        ]

    @staticmethod
    def validate_telegram_id(value):
        """
        Check if user with `telegram_id` exists in DB.
        Reference: https://www.django-rest-framework.org/api-guide/serializers/#field-level-validation
        """
        user = CustomUser.objects.filter(telegram_id=value).first()
        if not user:
            raise serializers.ValidationError(
                f"User with telegram_id={value} does not exist!"
            )
        return value


from rest_framework import serializers


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Detailed User model serializer.
    """

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "username",
            "telegram_id",
            "email",
            "first_name",
            "last_name",
            "profile_image",
            "is_active",
            "is_staff",
            "is_superuser",
            "last_login",
            "date_joined",
        )
