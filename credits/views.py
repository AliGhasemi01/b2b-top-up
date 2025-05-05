from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import CreditRequest
from .serializers import CreditRequestSerializer

class CreditRequestCreateView(generics.CreateAPIView):
    serializer_class = CreditRequestSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

class CreditRequestListView(generics.ListAPIView):
    serializer_class = CreditRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CreditRequest.objects.filter(seller=self.request.user).order_by('-created_at')
