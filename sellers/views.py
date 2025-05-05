from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import SellerProfileSerializer

class SellerProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = SellerProfileSerializer(request.user)
        return Response(serializer.data)

# Create your views here.
