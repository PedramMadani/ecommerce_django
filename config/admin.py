from django.contrib import admin
from .models import SiteSetting


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ['key', 'value', 'description']
    # Allow direct editing of the value field from the list view
    list_editable = ['value']
    search_fields = ['key', 'description']
    list_filter = ['key']
    fieldsets = (
        (None, {
            'fields': ('key', 'value', 'description'),
            'description': 'Modify the site settings. Be cautious as changes can affect site behavior.'
        }),
    )
