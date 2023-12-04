from django.contrib import admin
from .models import Notification
# Register your models here.

class CustomNotificationAdmin(admin.ModelAdmin):
    pass


admin.site.register(Notification, CustomNotificationAdmin)