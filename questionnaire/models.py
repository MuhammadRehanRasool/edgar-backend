from django.db import models

# Create your models here.

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
    price = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Subscription Types"

    def __str__(self):
        return self.get_title_display() + " ("+str(self.price)+"$)"


class Subject(models.Model):
    title = models.CharField(max_length=256)

    class Meta:
        verbose_name_plural = "Subjects"

    def __str__(self):
        return self.title


class Topic(models.Model):
    title = models.CharField(max_length=256)
    subject = models.ForeignKey(
        'Subject',
        on_delete=models.CASCADE,
    )
    subscription_types = models.ManyToManyField(SubscriptionTypes)

    class Meta:
        verbose_name_plural = "Topics"

    def __str__(self):
        return self.title + " ("+str(self.subject)+")"


# https://www.airplane.dev/blog/django-admin-crash-course-how-to-build-a-basic-admin-panel
