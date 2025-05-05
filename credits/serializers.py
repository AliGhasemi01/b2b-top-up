from rest_framework import serializers
from .models import CreditRequest

class CreditRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditRequest
        fields = ['id', 'amount', 'status', 'created_at']
        read_only_fields = ['status', 'created_at']