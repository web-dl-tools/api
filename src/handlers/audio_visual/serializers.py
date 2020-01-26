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
        fields = ('id', 'user', 'status', 'url', 'path', 'format_selection')
        read_only_fields = ('id', 'status')
        extra_kwargs = {
            'user': {
                'write_only': True
            }
        }
