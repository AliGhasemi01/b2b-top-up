from django.contrib import admin
from .models import CreditRequest, TopUpRequest, PhoneNumber, Status
from django.core.exceptions import ValidationError
import logging

logger = logging.getLogger(__name__)

@admin.register(CreditRequest)
class CreditRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'seller', 'amount', 'status', 'created_at', 'processed_at']
    list_filter = ['status', 'created_at', 'processed_at']
    search_fields = ['seller__username', 'seller__email', 'amount']
    ordering = ['-created_at']
    readonly_fields = ['processed_at']
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # editiing
            return ('seller', 'created_at', 'processed_at')
        else:    # creating
            return ('status', 'created_at', 'processed_at')

    actions = ['approve_requests', 'reject_requests']
    
    def approve_requests(self, request, queryset):
        for credit_request in queryset:
            try:
                credit_request.approve()
                self.message_user(request, "Selected requests approved successfully.")

            except Exception as e:
                self.message_user(request, f"Error approving request {credit_request.id}: {str(e)}", level='error')
        
    
    def reject_requests(self, request, queryset):
        for credit_request in queryset:
            try:
                credit_request.reject()
                self.message_user(request, "Selected requests rejected successfully.")
            except Exception as e:
                self.message_user(request, f"Error rejecting request {credit_request.id}: {str(e)}", level='error')
                
    def save_model(self, request, obj, form, change):
        logger.info(f"OBJ STATUS: {obj.status}")
        try:
            if not obj is None and obj.status == Status.APPROVED:
                obj.approve()
        except ValidationError as e:
            self.message_user(request, f"Error processing payment: {str(e)}", level='error')
            obj.delete()
            
        super().save_model(request, obj, form, change)


@admin.register(TopUpRequest)
class TopUpRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'seller', 'phone_number', 'amount', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('seller__username', 'amount')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        try:
            obj.process_payment()
        except ValidationError as e:
            self.message_user(request, f"Error processing payment: {str(e)}", level='error')
            obj.delete()
            
@admin.register(PhoneNumber)
class PhoneNumberAdmin(admin.ModelAdmin):
    list_display = ('id', 'number','seller', 'total_topup', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('number',)
    ordering = ('-created_at',)
    readonly_fields = ('total_topup', 'created_at', 'seller')
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # editiing
            return ('seller', 'total_topup', 'created_at')
        else:    # creating
            return ('total_topup', 'created_at')