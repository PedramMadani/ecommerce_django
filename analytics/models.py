from django.db import models
from products.models import Product
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db.models.fields.json import JSONField


class ProductView(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='views', verbose_name="Product")
    ip_address = models.CharField(max_length=20, verbose_name="IP Address")
    session = models.CharField(max_length=100, verbose_name="Session ID")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Created At")

    class Meta:
        verbose_name = "Product View"
        verbose_name_plural = "Product Views"


class UserActivity(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='activities', verbose_name="User")
    action = models.CharField(max_length=255, verbose_name="Action")
    # Use Django's JSONField for storing JSON data.
    details = JSONField(verbose_name="Details")
    timestamp = models.DateTimeField(
        auto_now_add=True, verbose_name="Timestamp")

    class Meta:
        verbose_name = "User Activity"
        verbose_name_plural = "User Activities"


class SocialShare(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='social_shares', verbose_name="User")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='shares', verbose_name="Product")
    platform = models.CharField(max_length=255, verbose_name="Platform")
    share_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Share Date")

    class Meta:
        verbose_name = "Social Share"
        verbose_name_plural = "Social Shares"
