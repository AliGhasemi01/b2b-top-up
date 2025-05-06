from django.db import models, transaction
from django.core.exceptions import ValidationError
from sellers.models import Seller
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

class CreditRequest(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'در حال بررسی'),
        ('APPROVED', 'تأیید شده'),
        ('REJECTED', 'رد شده'),
    ]
    
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='credit_requests')
    amount = models.PositiveBigIntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.seller.username} - {self.amount} تومان ({self.status})"
    
    def save(self, *args, **kwargs):
        if self.pk:
            old = CreditRequest.objects.get(pk=self.pk)
            if old.status == 'PENDING' and self.status == 'APPROVED' and self.processed_at is None:
                with transaction.atomic():
                    seller = Seller.objects.select_for_update().get(pk=self.seller.pk)
                    seller.credit += self.amount
                    seller.save()
                self.processed_at = timezone.now()
            elif old.status == 'PENDING' and self.status == 'REJECTED' and self.processed_at is None:
                self.processed_at = timezone.now()
        super().save(*args, **kwargs)
        
        
class TopUpRequest(models.Model):

    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='topup_requests')
    phone_number = models.CharField(max_length=15)
    amount = models.PositiveBigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.seller.username} → {self.phone_number} ({self.amount})"
    
    @classmethod
    def create_for(cls, seller, phone_number, amount):
        if amount <= 0:
            raise ValidationError("Amount must be positive.")
        
        if not phone_number or not phone_number.isdigit() or len(phone_number) != 11:
            raise ValidationError("Invalid phone number format.")


        with transaction.atomic():
            locked_seller = Seller.objects.select_for_update().get(pk=seller.pk)
            
            if locked_seller.credit < amount:
                raise ValidationError("Insufficient credit.")
            
            locked_seller.credit -= amount
            locked_seller.save()
            
            logger.info(f"[TopUpRequest] Seller: {seller.username} | Phone: {phone_number} | Amount: {amount} | Remaining Credit: {seller.credit}")
            
            return cls.objects.create(
                seller=locked_seller,
                phone_number=phone_number,
                amount=amount,
            )
