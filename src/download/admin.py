# """
# Download admin.
# """
# from django.contrib import admin
# from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin
#
# from .models import BaseRequest
# from src.handlers.youtube_dl.models import Request as YoutubeDlRequest
#
#
# class BaseRequestAdmin(PolymorphicChildModelAdmin):
#     """
#     Base request child model.
#     """
#     base_model = BaseRequest
#
#
# @admin.register(BaseRequest)
# class RequestAdmin(PolymorphicParentModelAdmin):
#     """
#     Base request admin.
#     """
#     base_model = BaseRequest
#     child_models = (BaseRequest, YoutubeDlRequest)
