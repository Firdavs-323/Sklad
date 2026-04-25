from django.db import models
from django.contrib.auth.models import User
from products.models import Product

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('in', 'Incoming'),
        ('out', 'Outgoing'),
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=3, choices=TRANSACTION_TYPES)
    quantity = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)
    performed_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.transaction_type == 'in':
            self.product.quantity += self.quantity
        elif self.transaction_type == 'out':
            if self.product.quantity >= self.quantity:
                self.product.quantity -= self.quantity
            else:
                raise ValueError("Insufficient stock")
        self.product.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.transaction_type} - {self.product.name} - {self.quantity}"
