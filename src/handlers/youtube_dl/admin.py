# """
# Youtube-dl admin.
# """
# from django.contrib import admin
#
# from .models import Request
# from src.download.admin import BaseRequestAdmin
#
#
# @admin.register(Request)
# class RequestAdmin(BaseRequestAdmin):
#     """
#     Request admin,
#     """
#     base_model = Request
