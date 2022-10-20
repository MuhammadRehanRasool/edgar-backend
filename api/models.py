import email
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


SUBSCRIPTION_TYPES = [
    ('DY', 'Day'),
    ('WY', 'Week'),
    ('MY', 'Month'),
    ('6Y', '6 Months'),
    ('YY', 'Year'),
]


class SubscriptionTypes(models.Model):
    title = models.CharField(
        max_length=2,
        choices=SUBSCRIPTION_TYPES
    )
    price = models.IntegerField()
    
    class Meta:
        verbose_name_plural = "Subscription Types"

    def __str__(self):
        return self.get_title_display() + " ("+str(self.price)+"$)"


class Subject(models.Model):
    title = models.CharField(max_length=256)
    subscription_types = models.ManyToManyField(SubscriptionTypes)
    
    class Meta:
        verbose_name_plural = "Subjects"

    def __str__(self):
        return self.title

# https://www.airplane.dev/blog/django-admin-crash-course-how-to-build-a-basic-admin-panel