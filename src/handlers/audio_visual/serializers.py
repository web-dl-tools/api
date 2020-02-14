"""
Audio visual handler serializers.

This file contains the serializer definition for the AudioVisualRequest model object.
"""
from rest_framework import serializers

from .models import AudioVisualRequest


class AudioVisualRequestSerializer(serializers.ModelSerializer):
    """
    Audio visual request serializer.
    """

    class Meta:
        """
        Serializer metadata.
        """

        model = AudioVisualRequest
        fields = (
            "id",
            "created_at",
            "modified_at",
            "user",
            "status",
            "url",
            "start_processing_at",
            "completed_at",
            "progress",
            "title",
            "data",
            "path",
            "status_display",
            "format_selection",
            "output",
        )
        read_only_fields = (
            "id",
            "created_at",
            "modified_at",
            "status",
            "start_processing_at",
            "completed_at",
            "progress",
            "title",
            "data",
            "path",
        )
        extra_kwargs = {"user": {"write_only": True}}
