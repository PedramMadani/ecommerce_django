from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.exceptions import ValidationError


def validate_positive(value):
    if value <= 0:
        raise ValidationError(
            '%(value)s is not a positive number', params={'value': value})


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    category = models.ForeignKey(
        Category, related_name='products', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255, db_index=True)
    description = models.TextField(blank=True)
    # Ensure uniqueness and allow blank
    slug = models.SlugField(unique=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(validators=[validate_positive])
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = original_slug = slugify(self.name)
            for i in range(1, 100):  # Just an arbitrary number for attempts
                if not Product.objects.filter(slug=self.slug).exists():
                    break
                self.slug = f'{original_slug}-{i}'
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProductAttribute(models.Model):
    product = models.ForeignKey(
        Product, related_name='attributes', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)  # e.g., "Color", "Size"
    value = models.CharField(max_length=100)  # e.g., "Red", "Large"

    def __str__(self):
        return f"{self.name} for {self.product.name}"


class ProductVariant(models.Model):
    product = models.ForeignKey(
        Product, related_name='variants', on_delete=models.CASCADE)
    sku = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    attributes = models.ManyToManyField(ProductAttribute)

    def __str__(self):
        return f"{self.product.name} - SKU {self.sku}"


class Tag(models.Model):
    name = models.CharField(max_length=100)
    products = models.ManyToManyField(Product, related_name='tags')

    def __str__(self):
        return self.name


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)

    def __str__(self):
        return f"Wishlist of {self.user.username}"


class ProductRecommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # Why is this product recommended?
    reason = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)


class StockChange(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    change = models.IntegerField()
    reason = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.change} units for {self.product.name} because {self.reason}"


class Inventory(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    low_stock_threshold = models.PositiveIntegerField()

    def __str__(self):
        return f"Inventory for {self.product.name}"
