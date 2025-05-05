from django.urls import path
from .views import CreditRequestCreateView, CreditRequestListView

urlpatterns = [
    path('request/', CreditRequestCreateView.as_view(), name='credit-request'),
    path('my-requests/', CreditRequestListView.as_view(), name='my-credit-requests'),
]