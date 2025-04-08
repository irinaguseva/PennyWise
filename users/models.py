from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    budget = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
