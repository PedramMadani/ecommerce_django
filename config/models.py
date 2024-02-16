from django.db import models


class SiteSetting(models.Model):
    TYPE_CHOICES = (
        ('int', 'Integer'),
        ('str', 'String'),
        ('bool', 'Boolean'),
    )
    key = models.CharField(max_length=255, unique=True)
    value = models.TextField()
    description = models.TextField(blank=True)
    type = models.CharField(max_length=4, choices=TYPE_CHOICES, default='str')

    def get_value(self):
        """Return value in correct type."""
        if self.type == 'int':
            return int(self.value)
        elif self.type == 'bool':
            return self.value.lower() in ('true', '1', 't')
        return self.value  # Default to string

    def __str__(self):
        return f"{self.key}: {self.value}"
