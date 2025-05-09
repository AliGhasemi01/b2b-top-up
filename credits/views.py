from django.shortcuts import render
from django.core.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import CreditRequest, TopUpRequest, PhoneNumber
from .serializers import CreditRequestSerializer, TopUpRequestSerializer, PhoneNumberSerializer
from rest_framework.status import HTTP_400_BAD_REQUEST
import logging

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

logger = logging.getLogger(__name__)

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
        logger.info(f"[TopUpRequest] User: {request.user.username} | Request Data: {request.data}")

        serializer = TopUpRequestSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            try:
                top_up = serializer.save()
                logger.info(f"[TopUpRequest] Created: {top_up}")
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                logger.error(f"[TopUpRequest] Error: {str(e)}")
                return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        logger.error(f"[TopUpRequest] Validation Error: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        top_up_requests = TopUpRequest.objects.filter(seller=request.user).order_by('-created_at')
        
        serializer = TopUpRequestSerializer(top_up_requests, many=True)
        return Response(serializer.data)
    
class PhoneNumberRequestView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = PhoneNumberSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            try:
                serializer.save(seller=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except ValidationError as e:
                return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
                
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        phone_number_requests = PhoneNumber.objects.filter(seller=request.user).order_by('-created_at')
        
        serializer = PhoneNumberSerializer(phone_number_requests, many=True)
        return Response(serializer.data)