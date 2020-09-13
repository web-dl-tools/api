"""
Download serializers.

This file contains serializer definitions for the BaseRequest and Log
as well as a PolymorphicRequestSerializer.
This file also acts as a registration of handler Request models and Serializer object bindings.
"""
from rest_framework import serializers
from rest_polymorphic.serializers import PolymorphicSerializer

from .models import BaseRequest, Log


class BaseRequestSerializer(serializers.ModelSerializer):
    """
    A base request serializer for the BaseRequest model object.
    """
    excluded_fields = (
        "data",
        "modified_at",
        "path",
        "user",
        "start_processing_at",
        "completed_at",
        "start_processing_at",
        "path",
    )

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

    @property
    def _readable_fields(self):
        """
        A generator for readable fields extended to add exclude field(s) functionality.
        """
        for key, field in self.fields.items():
            if "action" in self.context and self.context["action"] == "list" and key in self.excluded_fields:
                continue

            if not field.write_only:
                yield field


class PolymorphicRequestSerializer(PolymorphicSerializer):
    """
    A polymorphic request serializer containing all sub handlers
    as well as the parent BaseRequest and their serializers.
    This serializer object also acts as a registration definition
    of custom handler Requests models and Serializers objects and their bindings.
    """
    from src.handlers.audio_visual.models import AudioVisualRequest
    from src.handlers.direct.models import DirectRequest
    from src.handlers.torrent.models import TorrentRequest
    from src.handlers.resource.models import ResourceRequest
    from src.handlers.audio_visual.serializers import AudioVisualRequestSerializer
    from src.handlers.direct.serializers import DirectRequestSerializer
    from src.handlers.torrent.serializers import TorrentRequestSerializer
    from src.handlers.resource.serializers import ResourceRequestSerializer

    resource_type_field_name = "request_type"
    model_serializer_mapping = {
        BaseRequest: BaseRequestSerializer,
        AudioVisualRequest: AudioVisualRequestSerializer,
        DirectRequest: DirectRequestSerializer,
        TorrentRequest: TorrentRequestSerializer,
        ResourceRequest: ResourceRequestSerializer
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
