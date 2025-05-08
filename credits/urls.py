from django.urls import path
from .views import CreditRequestView, TopUpRequestView

urlpatterns = [
    path('credit-requests/', CreditRequestView.as_view(), name='credit-requests'),
    path('top-ups/', TopUpRequestView.as_view(), name='top-ups'),
]