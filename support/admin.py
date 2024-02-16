from django.contrib import admin
from .models import FAQ, SupportTicket, Notification


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'created_at']
    list_filter = ['created_at']
    search_fields = ['question', 'answer']
    date_hierarchy = 'created_at'


@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ['user', 'subject', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username', 'subject', 'message']
    list_editable = ['status']
    actions = ['mark_as_resolved']

    def mark_as_resolved(self, request, queryset):
        queryset.update(status='Resolved')
    mark_as_resolved.short_description = "Mark selected tickets as resolved"


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'message', 'read', 'timestamp']
    list_filter = ['read', 'timestamp']
    search_fields = ['user__username', 'message']
    list_editable = ['read']
