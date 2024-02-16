from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product
from shipping.models import ShippingOption
from promotions.models import Coupon
from .tasks import send_order_confirmation_email

User = get_user_model()


class PaymentStatus(models.TextChoices):
    COMPLETED = 'completed', 'Completed'
    FAILED = 'failed', 'Failed'
    # Add more as needed, ensure this is placed correctly within the context of use.


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
        ('returned', 'Returned'),
    ]

    def send_confirmation_email(self):
        # Call the Celery task
        send_order_confirmation_email.delay(self.user.email, self.id)

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    payment_status = models.CharField(
        max_length=50,
        choices=PaymentStatus.choices,
        default=PaymentStatus.COMPLETED,
    )

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Order {self.order.id})"


class Cart(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name='carts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        user_str = f"User {self.user.username}" if self.user else "Anonymous User"
        return f"Cart {self.id} - {user_str}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items',
                             on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name='cart_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Cart {self.cart.id})"
