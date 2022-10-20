from django.db import models

# Create your models here.

# SUBSCRIPTION_TYPES = [
#     ('DY', 'Day'),
#     ('WY', 'Week'),
#     ('MY', 'Month'),
#     ('6Y', '6 Months'),
#     ('YY', 'Year'),
# ]


class SubscriptionTypes(models.Model):
    title = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Subscription Types"

    def __str__(self):
        return str(self.title)


class Subject(models.Model):
    title = models.CharField(max_length=256)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Subjects"

    def __str__(self):
        return self.title


class Topic(models.Model):
    title = models.CharField(max_length=256)
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
    )
    subscription_types = models.ManyToManyField(
        SubscriptionTypes, related_name="subscription_types_with_price", through="TopicSubscription")
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Topics"

    def __str__(self):
        return self.title + " ("+str(self.subject)+")"


class TopicSubscription(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    subscription_types = models.ForeignKey(
        SubscriptionTypes, on_delete=models.CASCADE)
    price = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.topic) + " ("+str(self.subscription_types)+" - "+str(self.price)+"$)"


# https://www.airplane.dev/blog/django-admin-crash-course-how-to-build-a-basic-admin-panel
# https://www.youtube.com/watch?v=vD19E_HHfXI
