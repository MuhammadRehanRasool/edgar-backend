from pyexpat import model
from django.contrib import admin
from . import models
# Register your models here.


class TopicSubscriptionAdmin(admin.TabularInline):
    model = models.TopicSubscription
    extra = 1

class TopicAdmin(admin.ModelAdmin):
    inlines = [TopicSubscriptionAdmin]

    class Meta:
        model = models.Topic


admin.site.register(models.SubscriptionTypes)
admin.site.register(models.Subject)
admin.site.register(models.Levels)
admin.site.register(models.Topic, TopicAdmin)
admin.site.register(models.Questions)
