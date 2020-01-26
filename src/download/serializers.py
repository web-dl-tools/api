"""
Download serializers.

This file contains serializer definitions for the BaseRequest, Log as well as a PolymorphicRequestSerializer.
This file also acts as a registration of handler Request and Serializer bindings.
"""
from rest_framework import serializers
from rest_polymorphic.serializers import PolymorphicSerializer

from .models import BaseRequest, Log

from src.handlers.audio_visual.models import AudioVisualRequest
from src.handlers.audio_visual.serializers import AudioVisualRequestSerializer


class BaseRequestSerializer(serializers.ModelSerializer):
    """
    a Base request serializer for the BaseRequest model object.
    """
    class Meta:
        """
        Serializer metadata.
        See https://www.django-rest-framework.org/api-guide/serializers/
        """
        model = BaseRequest
        fields = ('id', 'user', 'status', 'url', 'path', )
        read_only_fields = ('id', 'status')
        extra_kwargs = {
            'user': {
                'write_only': True
            }
        }


class PolymorphicRequestSerializer(PolymorphicSerializer):
    """
    a Polymorphic request serializer contains all sub handlers als well as the parent BaseRequest and their serializers.
    This serializer object also acts as a registration of custom handler Requests and Serializers and their bindings.
    """
    resource_type_field_name = 'request_type'
    model_serializer_mapping = {
        BaseRequest: BaseRequestSerializer,
        AudioVisualRequest: AudioVisualRequestSerializer,
    }


class LogSerializer(serializers.ModelSerializer):
    """
    a Log serializer for the Log model object.
    """
    class Meta:
        """
        Serializer metadata.
        See https://www.django-rest-framework.org/api-guide/serializers/
        """
        model = Log
        fields = '__all__'
