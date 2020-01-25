"""
Download serializers.
"""
from rest_framework import serializers
from rest_polymorphic.serializers import PolymorphicSerializer

from .models import BaseRequest, Log

from src.handlers.audio_visual.models import AudioVisualRequest
from src.handlers.audio_visual.serializers import AudioVisualRequestSerializer


class BaseRequestSerializer(serializers.ModelSerializer):
    """
    Base request serializer.
    """
    class Meta:
        """
        Serializer metadata.
        """
        model = BaseRequest
        fields = ('id', 'user', 'status', 'url', )
        read_only_fields = ('id', 'status')
        extra_kwargs = {
            'user': {
                'write_only': True
            }
        }


class PolymorphicRequestSerializer(PolymorphicSerializer):
    """
    Polymorphic request serializer.
    """
    resource_type_field_name = 'request_type'
    model_serializer_mapping = {
        BaseRequest: BaseRequestSerializer,
        AudioVisualRequest: AudioVisualRequestSerializer,
    }


class LogSerializer(serializers.ModelSerializer):
    """
    Log serializer.
    """
    class Meta:
        """
        Log metadata.
        """
        model = Log
        fields = '__all__'
