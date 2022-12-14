from django.db import models
from traitlets import default
from authentication.models import CustomUsers

# Create your models here.


class SubscriptionTypes(models.Model):
    title = models.CharField(max_length=20)
    expiryHours = models.IntegerField(default=24)
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


class Levels(models.Model):
    title = models.CharField(max_length=1028)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Levels"

    def __str__(self):
        return str(self.title)

# Generic


class TopicSubscription(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    subscription_types = models.ForeignKey(
        SubscriptionTypes, on_delete=models.CASCADE)
    price = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Topic Subscription"

    def __str__(self):
        return str(self.topic) + " ("+str(self.subscription_types)+" - "+str(self.price)+"$)"


class StudentSubscription(models.Model):
    user = models.ForeignKey(CustomUsers, on_delete=models.CASCADE)
    type = models.ForeignKey(
        TopicSubscription, on_delete=models.CASCADE)
    isActive = models.BooleanField(default=True)
    isExpired = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Student Subscription"

    def __str__(self):
        return str(self.type) + " ("+str(self.user)+")"


class Questions(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    level = models.ForeignKey(Levels, on_delete=models.CASCADE)
    question = models.CharField(max_length=1028)
    optionA = models.CharField(max_length=1028)
    optionB = models.CharField(max_length=1028)
    optionC = models.CharField(max_length=1028)
    optionD = models.CharField(max_length=1028)
    answer = models.CharField(max_length=1028)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Questions"

    def __str__(self):
        return str(self.topic) + " ("+str(self.question) + ")"


# https://www.airplane.dev/blog/django-admin-crash-course-how-to-build-a-basic-admin-panel
# https://www.youtube.com/watch?v=vD19E_HHfXI
