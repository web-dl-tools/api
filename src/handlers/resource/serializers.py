"""
Resource handler serializers.

This file contains the serializer definition for the ResourceRequest model object.
"""
from .models import ResourceRequest

from src.download.serializers import BaseRequestSerializer


CUSTOM_FIELDS = ("extensions", "min_bytes")

class ResourceRequestSerializer(BaseRequestSerializer):
    """
    Resource request serializer.
    """
    excluded_fields = BaseRequestSerializer.excluded_fields + CUSTOM_FIELDS

    class Meta:
        """
        Serializer metadata.
        """

        model = ResourceRequest
        fields = BaseRequestSerializer.Meta.fields + CUSTOM_FIELDS
        read_only_fields = BaseRequestSerializer.Meta.read_only_fields
        extra_kwargs = {"user": {"write_only": True}}
