"""
Torrent handler serializers.

This file contains the serializer definition for the TorrentRequest model object.
"""
from .models import TorrentRequest

from src.download.serializers import BaseRequestSerializer


class TorrentRequestSerializer(BaseRequestSerializer):
    """
    Torrent request serializer.
    """

    class Meta:
        """
        Serializer metadata.
        """

        model = TorrentRequest
        fields = BaseRequestSerializer.Meta.fields
        read_only_fields = BaseRequestSerializer.Meta.read_only_fields
        extra_kwargs = {"user": {"write_only": True}}
