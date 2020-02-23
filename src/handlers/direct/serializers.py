"""
Direct handler serializers.

This file contains the serializer definition for the DirectRequest model object.
"""
from rest_framework import serializers

from .models import DirectRequest


class DirectRequestSerializer(serializers.ModelSerializer):
    """
    Direct request serializer.
    """

    class Meta:
        """
        Serializer metadata.
        """

        model = DirectRequest
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
