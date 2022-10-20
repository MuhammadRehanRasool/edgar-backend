from django.contrib import admin
from . import models
# Register your models here.

admin.site.site_header = "🎮 Game Quiz ✨"
admin.site.site_title = "Game Quiz Admin"

admin.site.register(models.Subject)
admin.site.register(models.Topic)
admin.site.register(models.SubscriptionTypes)

# Hide AUTHENTICATION AND AUTHORIZATION

from django.contrib.auth.models import User
from django.contrib.auth.models import Group

admin.site.unregister(User)
admin.site.unregister(Group)
