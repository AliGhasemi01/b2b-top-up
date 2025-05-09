from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Seller

@admin.register(Seller)
class SellerAdmin(UserAdmin):
    model = Seller
    list_display = ('username', 'email', 'credit', 'is_active', 'is_staff')
    
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('credit',)}),
    )