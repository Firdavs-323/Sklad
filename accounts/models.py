from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    ROLES = [
        ('admin', 'Admin'),
        ('warehouse_worker', 'Warehouse Worker'),
        ('store_employee', 'Store Employee'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLES, default='store_employee')

    def __str__(self):
        return f"{self.user.username} - {self.role}"
