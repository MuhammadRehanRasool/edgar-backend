from django.contrib.auth.models import Group
from django.contrib import admin
from . import models
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    exclude = ('first_name', 'last_name', 'groups', 'user_permissions',
               'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined')
    list_display = ('pk', 'username', 'email', 'name', 'is_admin')
    list_filter = ('is_staff','signedUpAt',)

    def is_admin(self, obj):
        pl = "✔️" if obj.is_staff else "❌"
        return pl

    # def is_online(self, obj):
    #     return obj.is_active


admin.site.register(models.CustomUsers, UserAdmin)


admin.site.site_header = "🎮 Game Quiz ✨"
admin.site.site_title = "Game Quiz Admin"
admin.site.index_title = "Website administration"


# Hide AUTHENTICATION AND AUTHORIZATION

# from django.contrib.auth.models import User

# admin.site.unregister(User)
admin.site.unregister(Group)
