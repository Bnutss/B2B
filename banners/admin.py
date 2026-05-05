from django.contrib import admin
from django.utils.html import format_html
from .models import Banner


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'is_active', 'preview']
    list_editable = ['order', 'is_active']

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" height="50" style="border-radius:4px"/>', obj.image.url)
        return '—'

    preview.short_description = 'Фото'
