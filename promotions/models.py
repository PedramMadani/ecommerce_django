from django.db import models
from products.models import Product
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.PositiveIntegerField(
        help_text='Percentage discount', validators=[MinValueValidator(1)])
    active = models.BooleanField()

    def __str__(self):
        return self.code


class Bundle(models.Model):
    name = models.CharField(max_length=255)
    products = models.ManyToManyField(Product)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    discount_rate = models.FloatField(
        help_text='Percentage discount for the bundle', validators=[MinValueValidator(0)])
    validity_period = models.DateTimeField()

    def __str__(self):
        return self.name


class AffiliateProgram(models.Model):
    name = models.CharField(max_length=255)
    commission_rate = models.DecimalField(
        max_digits=5, decimal_places=2, validators=[MinValueValidator(0)])
    description = models.TextField()

    def __str__(self):
        return self.name


class AffiliateLink(models.Model):
    affiliate_program = models.ForeignKey(
        AffiliateProgram, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    generated_link = models.URLField()
    clicks = models.PositiveIntegerField(default=0)
    registrations = models.PositiveIntegerField(default=0)
    purchases = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.affiliate_program.name}"


class LoyaltyPoints(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    points = models.PositiveIntegerField(default=0)
    earned_on = models.DateTimeField(auto_now_add=True)
    expires_on = models.DateTimeField()

    def __str__(self):
        return f"{self.user.username} - {self.points} points"
