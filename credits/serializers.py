from rest_framework import serializers
from .models import CreditRequest, TopUpRequest
from django.core.exceptions import ValidationError

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
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be positive.")
        return value
    
    def validate_phone_number(self, value):
        if not value or not value.isdigit() or len(value) != 11:
            raise serializers.ValidationError("Invalid phone number format.")
        return value
    
    def create(self, validated_data):
        seller = self.context['request'].user
        
        top_up_request = TopUpRequest.objects.create(
            seller=seller,
            phone_number=validated_data['phone_number'],
            amount=validated_data['amount']
        )
        
        try:
            top_up_request.process_payment()
            return top_up_request
        except ValidationError as e:
            top_up_request.delete()
            raise serializers.ValidationError(str(e))