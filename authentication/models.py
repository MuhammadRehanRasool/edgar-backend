from django.db import models

# Create your models here.

class Users(models.Model):
    name = models.CharField(max_length=256)
    username = models.CharField(
        max_length=64, unique=True)
    email = models.EmailField(
        max_length=256, unique=True)
    password = models.CharField(max_length=2048)

    class Meta:
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username