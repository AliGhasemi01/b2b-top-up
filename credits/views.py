from django.shortcuts import render
from django.core.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import CreditRequest, TopUpRequest
from .serializers import CreditRequestSerializer, TopUpRequestSerializer
from rest_framework.status import HTTP_400_BAD_REQUEST

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

class CreditRequestView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = CreditRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(seller=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        credit_requests = CreditRequest.objects.filter(seller=request.user).order_by('-created_at')
        
        serializer = CreditRequestSerializer(credit_requests, many=True)
        return Response(serializer.data)


class TopUpRequestView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = TopUpRequestSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            try:
                top_up = serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
                
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        top_up_requests = TopUpRequest.objects.filter(seller=request.user).order_by('-created_at')
        
        serializer = TopUpRequestSerializer(top_up_requests, many=True)
        return Response(serializer.data)