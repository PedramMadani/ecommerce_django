from django.contrib import admin
from .models import Order, OrderItem, Cart, CartItem
from django.utils.html import format_html
from django.urls import reverse


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    # Use raw_id_fields for better performance with a large number of products
    raw_id_fields = ['product']
    extra = 0  # No extra empty forms


class CartItemInline(admin.TabularInline):
    model = CartItem
    raw_id_fields = ['product']
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at', 'status', 'total_price',
                    'payment_status', 'shipping_option_display', 'order_detail_link']
    list_filter = ['status', 'created_at', 'payment_status']
    inlines = [OrderItemInline]
    search_fields = ['user__username']

    date_hierarchy = 'created_at'

    def shipping_option_display(self, obj):
        return obj.shipping_option.name if obj.shipping_option else 'N/A'
    shipping_option_display.short_description = 'Shipping Option'

    def order_detail_link(self, obj):
        url = reverse('admin:orders_order_change', args=[obj.id])
        return format_html(f'<a href="{url}">View Details</a>')
    order_detail_link.short_description = 'Order Details'


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at', 'updated_at']
    inlines = [CartItemInline]
    search_fields = ['user__username']

# Optionally, if you want to manage CartItem and OrderItem directly from the admin


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity']
    search_fields = ['cart__id', 'product__name']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'price', 'quantity']
    search_fields = ['order__id', 'product__name']
