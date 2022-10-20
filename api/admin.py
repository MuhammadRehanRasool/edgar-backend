from django.contrib import admin
from . import models
# Register your models here.

admin.site.site_header = "🎮 Game Quiz ✨"
admin.site.site_title = "Game Quiz Admin"

admin.site.register(models.Users)
admin.site.register(models.SubscriptionTypes)
admin.site.register(models.Subject)
