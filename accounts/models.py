# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class Profile(AbstractUser):
    # Add any additional fields you want here
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username
