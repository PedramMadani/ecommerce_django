from django.contrib import admin
from .models import Category, Product, ProductAttribute, ProductVariant, Tag, Wishlist, ProductRecommendation, StockChange, Inventory

# Inline classes allow editing of related records directly within the Product admin


class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 0  # Number of extra forms to display


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 0


class StockChangeInline(admin.TabularInline):
    model = StockChange
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    # Auto-populates slug field from name
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price',
                    'stock', 'available', 'created_at', 'is_active']
    list_filter = ['available', 'created_at', 'category', 'is_active']
    # Allow editing directly in the list view
    list_editable = ['price', 'stock', 'available', 'is_active']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductAttributeInline, ProductVariantInline,
               StockChangeInline]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user']
    filter_horizontal = ['products']  # For many-to-many fields


@admin.register(ProductRecommendation)
class ProductRecommendationAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'reason', 'created_at']
    list_filter = ['created_at']
    search_fields = ['reason']


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity', 'low_stock_threshold']


@admin.register(StockChange)
class StockChangeAdmin(admin.ModelAdmin):
    list_display = ['product', 'change', 'reason', 'created_at']
    list_filter = ['created_at']
    search_fields = ['reason', 'product__name']
