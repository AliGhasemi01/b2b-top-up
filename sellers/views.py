from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import SellerSignupSerializer, SellerProfileSerializer
from .models import Seller

class SellerSignupView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = SellerSignupSerializer(data=request.data)
        
        if serializer.is_valid():
            seller = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SellerProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        serializer = SellerProfileSerializer(request.user)
        return Response(serializer.data)