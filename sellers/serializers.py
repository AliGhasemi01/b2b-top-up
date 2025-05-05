from rest_framework import serializers
from .models import Seller

class SellerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = ['id', 'username', 'email', 'credit', 'company_name']
