"""
Direct handler serializers.

This file contains the serializer definition for the DirectRequest model object.
"""
from .models import DirectRequest

from src.download.serializers import BaseRequestSerializer


class DirectRequestSerializer(BaseRequestSerializer):
    """
    Direct request serializer.
    """

    class Meta:
        """
        Serializer metadata.
        """

        model = DirectRequest
        fields = BaseRequestSerializer.Meta.fields
        read_only_fields = BaseRequestSerializer.Meta.read_only_fields
        extra_kwargs = {"user": {"write_only": True}}
