from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

# Validator for phone numbers
phone_regex = RegexValidator(
    regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")


def user_directory_path(instance, filename):
    """file will be uploaded to MEDIA_ROOT/user_<id>/<filename>"""
    return f'user_{instance.user.id}/{filename}'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField(max_length=500, blank=True)
    phone = models.CharField(
        validators=[phone_regex], max_length=17, blank=True)
    avatar = models.ImageField(
        upload_to=user_directory_path, null=True, blank=True, default='default.jpg')


class UserAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    is_default = models.BooleanField(default=False)
