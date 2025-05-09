from django.urls import path
from .views import CreditRequestView, TopUpRequestView, PhoneNumberRequestView

urlpatterns = [
    path('credit-requests/', CreditRequestView.as_view(), name='credit-requests'),
    path('top-ups/', TopUpRequestView.as_view(), name='top-ups'),
    path('phone-numbers/', PhoneNumberRequestView.as_view(), name='phone-numbers'),
]