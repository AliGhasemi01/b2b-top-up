from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Seller
from .serializers import SellerSignupSerializer, SellerProfileSerializer


class SellerSignupView(generics.CreateAPIView):
    queryset = Seller.objects.all()
    serializer_class = SellerSignupSerializer

class SellerProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = SellerProfileSerializer(request.user)
        return Response(serializer.data)
