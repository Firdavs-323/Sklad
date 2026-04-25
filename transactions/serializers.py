from rest_framework import serializers
from .models import Transaction
from products.serializers import ProductSerializer

class TransactionSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    performed_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Transaction
        fields = '__all__'