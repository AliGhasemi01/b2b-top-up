from django.db import models, transaction
from django.core.exceptions import ValidationError
from sellers.models import Seller
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

class Status(models.IntegerChoices):
    PENDING = 0, 'Pending'
    APPROVED = 1, 'Approved'
    REJECTED = 2, 'Rejected'
    
class PhoneNumber(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='phone_numbers')
    number = models.CharField(max_length=15, unique=True)
    total_topup = models.DecimalField(max_digits=16, decimal_places=4, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.number

class CreditRequest(models.Model):
    
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='credit_requests')
    amount = models.DecimalField(max_digits=16, decimal_places=4)
    status = models.IntegerField(choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)

    
    def __str__(self):
        return f"{self.seller.username} - {self.amount} تومان - {self.get_status_display()}"
        
    def approve(self):
        try:
            with transaction.atomic():
                request = CreditRequest.objects.select_for_update().get(pk=self.pk)
                if request.status != Status.PENDING:
                    raise ValidationError("Cannot approve a non-pending request.")
                
                seller = Seller.objects.select_for_update().get(pk=self.seller.pk)
                seller.credit += self.amount
                seller.save(update_fields=['credit'])
                
                request.status = Status.APPROVED
                request.processed_at = timezone.now()
                request.save(update_fields=['status', 'processed_at'])
        except ValidationError as e:
            logger.error(f"[CreditRequest] Validation Error: {str(e)}")
            raise Exception(f"Error approving request: {str(e)}")
    
    def reject(self):
        try:
            with transaction.atomic():
                request = CreditRequest.objects.select_for_update().get(pk=self.pk)
                if request.status != Status.PENDING:
                    raise ValidationError("Cannot reject a non-pending request.")
                request.status = Status.REJECTED.value
                request.processed_at = timezone.now()
                request.save(update_fields=['status', 'processed_at'])
        except ValidationError as e:
            logger.error(f"[CreditRequest] Validation Error: {str(e)}")
            raise Exception(f"Error rejecting request: {str(e)}")
        
class TopUpRequest(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='topup_requests')
    phone_number = models.ForeignKey(PhoneNumber, on_delete=models.CASCADE, related_name='topup_requests')
    amount = models.DecimalField(max_digits=16, decimal_places=4)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.seller.username} → {self.phone_number} ({self.amount})"
    
    def process_payment(self):
        try:
            with transaction.atomic():
                locked_seller = Seller.objects.select_for_update().get(pk=self.seller.pk)
                locked_phone_number = PhoneNumber.objects.select_for_update().get(pk=self.phone_number.pk)

                if locked_seller != locked_phone_number.seller:
                    raise ValidationError("This phone number does not belong to this user.")

                if locked_seller.credit < self.amount:
                    raise ValidationError("Insufficient credit.")
                
                locked_seller.credit -= self.amount
                locked_seller.save(update_fields=['credit'])
                
                locked_phone_number.total_topup += self.amount
                locked_phone_number.save(update_fields=['total_topup'])
                
                logger.info(f"[TopUpRequest] Seller: {self.seller.username} | Phone: {self.phone_number} | Amount: {self.amount} | Remaining Credit: {locked_seller.credit}")
                return True
        except ValidationError as e:
            logger.error(f"[TopUpRequest] Validation Error: {str(e)}")
            raise Exception(f"Error processing payment: {str(e)}")
        