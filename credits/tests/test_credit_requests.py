from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from credits.models import CreditRequest, TopUpRequest, PhoneNumber
from rest_framework.exceptions import ValidationError


User = get_user_model()

class CreditRequestTests(TestCase):
    def setUp(self):
        self.seller1 = User.objects.create_user(username='seller1', password='testpass')
        self.seller2 = User.objects.create_user(username='seller2', password='testpass')

    def test_approved_credit_requests_add_credit(self):
        for i in range(1, 11):
            credit_request = CreditRequest.objects.create(seller=self.seller1, amount=i*1000)
            credit_request.approve()
            
            credit_request2 = CreditRequest.objects.create(seller=self.seller2, amount=i*10000)
            credit_request2.approve()
            

        self.seller1.refresh_from_db()
        self.assertEqual(self.seller1.credit, 55000)
        
        self.seller2.refresh_from_db()
        self.assertEqual(self.seller2.credit, 550000)

    def test_rejected_credit_requests_dont_add_credit(self):
        for i in range(1, 11):
            credit_request = CreditRequest.objects.create(seller=self.seller1, amount=i*1000)
            credit_request.reject()
            
            credit_request2 = CreditRequest.objects.create(seller=self.seller2, amount=i*10000)
            credit_request2.reject()
            
        self.seller1.refresh_from_db()
        self.assertEqual(self.seller1.credit, 0)
        
        self.seller2.refresh_from_db()
        self.assertEqual(self.seller2.credit, 0)
        
class topup_request_tests(TestCase):
    def setUp(self):
        self.seller = User.objects.create_user(username='testuser', password='testpass')
        self.phone_number = PhoneNumber.objects.create(seller=self.seller, number='09121234567')
        self.seller.credit = 50000
        self.seller.save()

    def test_successful_topup_request_reduces_credit(self):
        
        for i in range(1, 1001):
            topup_request = TopUpRequest.objects.create(
                seller=self.seller,
                phone_number=self.phone_number,
                amount=50
            )
            topup_request.process_payment()
        
        self.seller.refresh_from_db()
        self.assertEqual(self.seller.credit, 0)
        
    def test_failed_topup_request_does_not_reduce_credit(self):
        topup_request = TopUpRequest.objects.create(
            seller=self.seller,
            phone_number=self.phone_number,
            amount=100000
        )
        with self.assertRaises(Exception):
            topup_request.process_payment()
            
        self.seller.refresh_from_db()
        self.assertEqual(self.seller.credit, 50000)
        
    def test_phone_number_belongs_to_seller(self):
        other_seller = User.objects.create_user(username='otheruser', password='testpass')
        other_phone_number = PhoneNumber.objects.create(seller=other_seller, number='09909099090')
        
        topup_request = TopUpRequest(seller=self.seller, phone_number=other_phone_number, amount=50)
        
        with self.assertRaises(Exception):
            topup_request.process_payment()
            
    