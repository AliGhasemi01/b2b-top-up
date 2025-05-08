from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from credits.models import CreditRequest, Status


User = get_user_model()

class CreditRequestTests(TestCase):
    def setUp(self):
        self.seller1 = User.objects.create_user(username='seller1', password='testpass')
        self.seller2 = User.objects.create_user(username='seller2', password='testpass')

    def test_approved_credit_requests_add_credit(self):
        for _ in range(10):
            CreditRequest.objects.create(
                seller=self.seller1,
                amount=10000,
                status=Status.APPROVED,
                processed_at=timezone.now()
            )
            self.seller1.credit += 10000
            self.seller1.save()

        self.seller1.refresh_from_db()
        self.assertEqual(self.seller1.credit, 100000)
