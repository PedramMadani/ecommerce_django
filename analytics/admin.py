from django.contrib import admin
from .models import ProductView, UserActivity, SocialShare


@admin.register(ProductView)
class ProductViewAdmin(admin.ModelAdmin):
    list_display = ['product', 'ip_address', 'session', 'created_at']
    list_filter = ['created_at', 'product']
    search_fields = ['product__name', 'ip_address', 'session']
    date_hierarchy = 'created_at'  # Allows filtering by date hierarchically
    readonly_fields = ['ip_address', 'session',
                       'created_at']  # Prevents modification


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'timestamp']
    list_filter = ['action', 'timestamp']
    search_fields = ['user__username', 'action', 'details']
    date_hierarchy = 'timestamp'
    readonly_fields = ['user', 'action', 'details', 'timestamp']


@admin.register(SocialShare)
class SocialShareAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'platform', 'share_date']
    list_filter = ['platform', 'share_date']
    search_fields = ['user__username', 'product__name', 'platform']
    date_hierarchy = 'share_date'
    readonly_fields = ['user', 'product', 'platform', 'share_date']
