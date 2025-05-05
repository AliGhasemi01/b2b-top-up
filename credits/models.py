from django.db import models
from sellers.models import Seller

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