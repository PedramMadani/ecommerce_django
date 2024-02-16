from django.db import models
from orders.models import Order


class Payment(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=100)  # "Stripe" or "PayPal"
    transaction_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Status(models.TextChoices):
        COMPLETED = 'completed', 'Completed'
        FAILED = 'failed', 'Failed'
        PENDING = 'pending', 'Pending'

    status = models.CharField(
        max_length=50, choices=Status.choices, default=Status.PENDING)

    def __str__(self):
        return f"{self.payment_method} - {self.status} - Order {self.order.id}"
