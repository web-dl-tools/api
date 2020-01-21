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
        fields = ('username', 'first_name', 'last_name', 'email', 'last_login', 'date_joined')
