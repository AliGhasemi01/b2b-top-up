from django.urls import path
from .views import CreditRequestCreateView, CreditRequestListView, TopUpRequestCreateView, TopUpRequestListView

urlpatterns = [
    path('credit-request/', CreditRequestCreateView.as_view(), name='credit-request'),
    path('my-credit-requests/', CreditRequestListView.as_view(), name='my-credit-requests'),
    path('topup/', TopUpRequestCreateView.as_view(), name='topup-request'),
    path('my-topup-request/', TopUpRequestListView.as_view(), name='my-topup-requests'),
]