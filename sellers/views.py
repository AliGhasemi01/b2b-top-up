from django.shortcuts import render
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Seller
from .serializers import SellerSignupSerializer, SellerProfileSerializer


class SellerSignupView(CreateAPIView):
    queryset = Seller.objects.all()
    serializer_class = SellerSignupSerializer

class SellerProfileView(RetrieveAPIView):
    serializer_class = SellerProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
