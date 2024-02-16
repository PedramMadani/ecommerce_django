from django.contrib import admin
from .models import Coupon, Bundle, AffiliateProgram, AffiliateLink


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'valid_from', 'valid_to', 'discount', 'active']
    list_filter = ['active', 'valid_from', 'valid_to']
    search_fields = ['code']
    date_hierarchy = 'valid_from'
    list_editable = ['discount', 'active']
    actions = ['make_active', 'make_inactive']

    def make_active(self, request, queryset):
        queryset.update(active=True)
    make_active.short_description = "Mark selected coupons as active"

    def make_inactive(self, request, queryset):
        queryset.update(active=False)
    make_inactive.short_description = "Mark selected coupons as inactive"


@admin.register(Bundle)
class BundleAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'discount_rate', 'validity_period']
    search_fields = ['name']
    list_filter = ['validity_period']
    filter_horizontal = ['products']


@admin.register(AffiliateProgram)
class AffiliateProgramAdmin(admin.ModelAdmin):
    list_display = ['name', 'commission_rate', 'description']
    list_editable = ['commission_rate']


@admin.register(AffiliateLink)
class AffiliateLinkAdmin(admin.ModelAdmin):
    list_display = ['affiliate_program', 'user',
                    'generated_link', 'clicks', 'registrations', 'purchases']
    list_filter = ['affiliate_program', 'user']
    search_fields = ['affiliate_program__name',
                     'user__username', 'generated_link']
