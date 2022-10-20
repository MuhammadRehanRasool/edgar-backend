from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class CustomUsers(AbstractUser):
    name = models.CharField(max_length=256)
    username = models.CharField(
        max_length=64, unique=True)
    email = models.EmailField(
        max_length=256, unique=True)
    password = models.CharField(max_length=2048)
    signedUpAt = models.DateTimeField(verbose_name="joining date", auto_now_add=True)

    class Meta:
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username
