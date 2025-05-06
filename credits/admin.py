from django.contrib import admin
from .models import CreditRequest, TopUpRequest

@admin.register(CreditRequest)
class CreditRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'seller', 'amount', 'status', 'created_at', 'processed_at')
    list_filter = ('status', 'created_at')
    search_fields = ('seller__username',)
    ordering = ('-created_at',)
    
@admin.register(TopUpRequest)
class TopUpRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'seller', 'phone_number', 'amount', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('seller__username', 'phone_number')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)