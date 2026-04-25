from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product
from notifications.models import Notification
from accounts.models import Profile

@receiver(post_save, sender=Product)
def check_low_stock(sender, instance, **kwargs):
    if instance.quantity < 10:
        # Notify all admins and warehouse workers
        profiles = Profile.objects.filter(role__in=['admin', 'warehouse_worker'])
        for profile in profiles:
            Notification.objects.create(
                user=profile.user,
                message=f"Low stock alert: {instance.name} has only {instance.quantity} units remaining."
            )