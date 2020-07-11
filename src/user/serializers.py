"""
User serializers.

This file contains a serializer for the custom User model object.
"""
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    A user serializer extending the Django serializer in order
    to use the already defined serializer configuration
    for the Django admin fields already present on the custom User model.
    """

    class Meta:
        """
        Serializer metadata.
        See https://www.django-rest-framework.org/api-guide/serializers/
        """

        model = User
        fields = (
            "username",
            "password",
            "first_name",
            "last_name",
            "email",
            "last_login",
            "date_joined",
            "full_name",
        )
        read_only_fields = (
            "id",
            "last_login",
            "is_superuser",
            "is_staff",
            "is_active",
            "date_joined",
            "modified_at",
            "full_name",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        """
        Overwrite the create function to ensure the password is encrypted correctly.

        :param validated_data: a dict containing user field data.
        :return: a User model object
        """
        user = User.objects.create_user(**validated_data)
        return user
