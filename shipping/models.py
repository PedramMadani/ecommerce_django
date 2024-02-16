from django.db import models


class ShippingOption(models.Model):
    name = models.CharField(max_length=100)
    cost = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="Cost in USD")
    duration = models.CharField(
        max_length=100, help_text="Estimated delivery time")

    def __str__(self):
        return f"{self.name} - {self.duration} - ${self.cost}"
