from django.shortcuts import render
from django.core.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import CreditRequest, TopUpRequest
from .serializers import CreditRequestSerializer, TopUpRequestSerializer

class CreditRequestCreateView(CreateAPIView):
    serializer_class = CreditRequestSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

class CreditRequestListView(ListAPIView):
    serializer_class = CreditRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CreditRequest.objects.filter(seller=self.request.user).order_by('-created_at')

class TopUpRequestCreateView(CreateAPIView):
    serializer_class = TopUpRequestSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            amount = int(request.data.get('amount'))
            phone_number = request.data.get('phone_number')

            print("phone:", phone_number)
            print("amount:", amount)
            print("credit:", request.user.credit)
            
            topup = TopUpRequest.create_for(
                seller=request.user,
                phone_number=phone_number,
                amount=amount
            )
        except (TypeError, ValueError):
            return Response({'detail': 'Invalid input.'}, status=400)
        except ValidationError as e:
            return Response({'detail': str(e)}, status=400)

        serializer = self.get_serializer(topup)
        return Response(serializer.data)


class TopUpRequestListView(ListAPIView):
    serializer_class = TopUpRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TopUpRequest.objects.filter(seller=self.request.user).order_by('-created_at')