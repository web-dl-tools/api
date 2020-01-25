"""
User serializers.
"""
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    User serializer.
    """
    class Meta:
        """
        Serializer metadata.
        """
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'email', 'last_login', 'date_joined')
        read_only_fields = ('id', 'last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined', 'modified_at')
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        """
        Create a user entity and encode the password correctly.

        :param validated_data: dict
        :return: User
        """
        user = User.objects.create_user(**validated_data)
        return user
