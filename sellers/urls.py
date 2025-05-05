from django.urls import path
from .views import SellerSignupView, SellerProfileView

urlpatterns = [
    path('signup/', SellerSignupView.as_view(), name='seller-signup'),
    path('profile/', SellerProfileView.as_view(), name='seller-profile'),
]