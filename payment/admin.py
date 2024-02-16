from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['order', 'amount', 'payment_method',
                    'transaction_id', 'status', 'created_at']
    list_filter = ['payment_method', 'status', 'created_at']
    search_fields = ['order__id', 'transaction_id']
    date_hierarchy = 'created_at'  # Enables filtering by date easily
    readonly_fields = ['order', 'amount', 'payment_method', 'transaction_id',
                       'status', 'created_at']  # Assuming payments shouldn't be edited manually

    def has_add_permission(self, request, obj=None):
        # Typically, new payments should come from the actual payment process, not admin creation
        return False

    def has_delete_permission(self, request, obj=None):
        # Consider carefully if payments should be deletable; often, they should not be
        return False
