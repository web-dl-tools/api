"""
Torrent handler serializers.

This file contains the serializer definition for the TorrentRequest model object.
"""
from rest_framework import serializers

from .models import TorrentRequest


class TorrentRequestSerializer(serializers.ModelSerializer):
    """
    Torrent request serializer.
    """

    class Meta:
        """
        Serializer metadata.
        """

        model = TorrentRequest
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
