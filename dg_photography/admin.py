from django.contrib import admin
from .models import (
    Photo,
)

# Registered dg_photography models


class PhotoAdmin(admin.ModelAdmin):
    list = ("title", "camera_make", "camera_model", "year_taken")

    admin.site.register(Photo)
