from django.contrib import admin
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['product', 'transaction_type', 'quantity', 'date', 'performed_by']
    list_filter = ['transaction_type', 'date', 'performed_by']
    search_fields = ['product__name']
