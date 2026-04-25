from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'message', 'date', 'read']
    list_filter = ['read', 'date']
    search_fields = ['user__username', 'message']
