from django.contrib import admin
from .models import CreditRequest, TopUpRequest

@admin.register(CreditRequest)
class CreditRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'seller', 'amount', 'status', 'created_at', 'processed_at', 'get_status_display']
    list_filter = ['status', 'created_at', 'processed_at']
    search_fields = ['seller__username', 'seller__email', 'amount']
    ordering = ['-created_at']
    readonly_fields = ['processed_at']
    
    actions = ['approve_requests', 'reject_requests']
    
    def approve_requests(self, request, queryset):
        for credit_request in queryset:
            try:
                credit_request : CreditRequest
                credit_request.approve()
                self.message_user(request, "Selected requests approved successfully.")

            except Exception as e:
                self.message_user(request, f"Error approving request {credit_request.id}: {str(e)}", level='error') ##### CHECK
        
    
    def reject_requests(self, request, queryset):
        for credit_request in queryset:
            try:
                credit_request : CreditRequest
                credit_request.reject()
                self.message_user(request, "Selected requests rejected successfully.")
            except Exception as e:
                self.message_user(request, f"Error rejecting request {credit_request.id}: {str(e)}", level='error')


@admin.register(TopUpRequest)
class TopUpRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'seller', 'phone_number', 'amount', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('seller__username', 'phone_number')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)