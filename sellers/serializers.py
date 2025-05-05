from rest_framework import serializers
from .models import Seller
from django.contrib.auth.password_validation import validate_password


class SellerSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Seller
        fields = ['username', 'email', 'company_name', 'password', 'password2']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = Seller.objects.create_user(**validated_data)
        return user

class SellerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = ['id', 'username', 'email', 'credit', 'company_name']
