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


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Detailed User model serializer.
    """

    disk_space_used = serializers.DecimalField(max_digits=6, decimal_places=1)

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
            "disk_quota",
            "disk_space_used",
            "is_active",
            "is_staff",
            "is_superuser",
            "last_login",
            "date_joined",
        )

    def to_representation(self, instance):
        """
        Deliver consistent relative URLs of profile images.
        Issue: https://forum.djangoproject.com/t/drf-imagefield-serializes-entire-url-with-domain-name/6975
        """
        ret = super().to_representation(instance)
        ret["profile_image"] = (
            instance.profile_image.url if instance.profile_image else ""
        )
        return ret
