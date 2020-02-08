"""
Download serializers.

This file contains serializer definitions for the BaseRequest and Log
as well as a PolymorphicRequestSerializer.
This file also acts as a registration of handler Request models and Serializer object bindings.
"""
from rest_framework import serializers
from rest_polymorphic.serializers import PolymorphicSerializer

from .models import BaseRequest, Log

from src.handlers.audio_visual.models import AudioVisualRequest
from src.handlers.audio_visual.serializers import AudioVisualRequestSerializer


class BaseRequestSerializer(serializers.ModelSerializer):
    """
    A base request serializer for the BaseRequest model object.
    """

    class Meta:
        """
        Serializer metadata.
        See https://www.django-rest-framework.org/api-guide/serializers/
        """

        model = BaseRequest
        fields = (
            "id",
            "created_at",
            "modified_at",
            "user",
            "status",
            "status_display",
            "url",
            "start_processing_at",
            "completed_at",
            "title",
            "data",
            "path",
        )
        read_only_fields = (
            "id",
            "created_at",
            "modified_at",
            "status",
            "start_processing_at",
            "completed_at",
            "title",
            "data",
            "path",
        )
        extra_kwargs = {"user": {"write_only": True}}


class PolymorphicRequestSerializer(PolymorphicSerializer):
    """
    A polymorphic request serializer containing all sub handlers
    as well as the parent BaseRequest and their serializers.
    This serializer object also acts as a registration definition
    of custom handler Requests models and Serializers objects and their bindings.
    """

    resource_type_field_name = "request_type"
    model_serializer_mapping = {
        BaseRequest: BaseRequestSerializer,
        AudioVisualRequest: AudioVisualRequestSerializer,
    }


class LogSerializer(serializers.ModelSerializer):
    """
    A log serializer for the Log model object.
    """

    class Meta:
        """
        Serializer metadata.
        See https://www.django-rest-framework.org/api-guide/serializers/
        """

        model = Log
        fields = ("id", "created_at", "level", "level_display", "message")
