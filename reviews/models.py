from django.db import models
from django.contrib.auth.models import User
from products.models import Product
import json


class Review(models.Model):
    product = models.ForeignKey(
        Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.PositiveSmallIntegerField(help_text="Rating from 1 to 5")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review by {self.user.username} for {self.product.name}'


class Survey(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class SurveyResponse(models.Model):
    survey = models.ForeignKey(
        Survey, related_name='responses', on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    responses = models.JSONField(default=dict)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Response by {self.user.username if self.user else 'Anonymous'} for {self.survey.title}"
