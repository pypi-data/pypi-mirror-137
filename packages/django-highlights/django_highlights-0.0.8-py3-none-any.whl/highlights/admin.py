from django.contrib import admin

from .models import Highlight


@admin.register(Highlight)
class HighlightAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ("maker", "created", "content", "object_id")
