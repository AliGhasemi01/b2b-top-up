from django.contrib import admin
from .models import CreditRequest

@admin.register(CreditRequest)
class CreditRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'seller', 'amount', 'status', 'created_at', 'processed_at')
    list_filter = ('status', 'created_at')
    search_fields = ('seller__username',)
    ordering = ('-created_at',)