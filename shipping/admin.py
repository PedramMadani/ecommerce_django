from django.contrib import admin
from .models import ShippingOption


@admin.register(ShippingOption)
class ShippingOptionAdmin(admin.ModelAdmin):
    list_display = ['name', 'cost', 'duration']
    # Allow for easy editing right from the list display
    list_editable = ['cost', 'duration']
    search_fields = ['name']
    # Filtering options can help quickly find shipping options based on cost or duration
    list_filter = ['cost', 'duration']

    def has_add_permission(self, request, obj=None):
        # Assuming adding new shipping options is allowed
        return True

    def has_change_permission(self, request, obj=None):
        # Assuming changing existing shipping options is allowed
        return True

    def has_delete_permission(self, request, obj=None):
        # Consider if you want to allow deleting shipping options directly from admin
        # This might depend on whether shipping options are tightly integrated with orders
        return True
