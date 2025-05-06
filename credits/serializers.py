from rest_framework import serializers
from .models import CreditRequest, TopUpRequest

class CreditRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditRequest
        fields = ['id', 'amount', 'status', 'created_at']
        read_only_fields = ['status', 'created_at']

class TopUpRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopUpRequest
        fields = ['id', 'phone_number', 'amount', 'created_at']
        read_only_fields = ['created_at']
