from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from credits.models import CreditRequest, TopUpRequest

User = get_user_model()

class TopUpTests(TestCase):
    def setUp(self):
        self.seller = User.objects.create_user(username='testuser', password='pass', credit=50000)

    def test_successful_topup_request_reduces_credit(self):
        topup = TopUpRequest.create_for(
            seller=self.seller,
            phone_number='09121234567',
            amount=10000
        )
        self.seller.refresh_from_db()
        self.assertEqual(self.seller.credit, 40000)