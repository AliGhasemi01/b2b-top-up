from django.db import models
from django.contrib.auth.models import AbstractUser

class Seller(AbstractUser):
    company_name = models.CharField(max_length=100, blank=True)
    credit = models.BigIntegerField(default=0)

    def __str__(self):
        return f"{self.username} - {self.credit} تومان"


# Create your models here.
