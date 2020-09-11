"""
Audio visual handler serializers.

This file contains the serializer definition for the AudioVisualRequest model object.
"""
from .models import AudioVisualRequest

from src.download.serializers import BaseRequestSerializer

CUSTOM_FIELDS = ("format_selection", "output")

class AudioVisualRequestSerializer(BaseRequestSerializer):
    """
    Audio visual request serializer.
    """
    excluded_fields = BaseRequestSerializer.excluded_fields + CUSTOM_FIELDS

    class Meta:
        """
        Serializer metadata.
        """

        model = AudioVisualRequest
        fields = BaseRequestSerializer.Meta.fields + CUSTOM_FIELDS
        read_only_fields = BaseRequestSerializer.Meta.read_only_fields
        extra_kwargs = {"user": {"write_only": True}}
