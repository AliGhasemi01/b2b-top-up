import threading
import time
import requests

from django.test import LiveServerTestCase
from django.contrib.auth import get_user_model
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from credits.models import PhoneNumber

User = get_user_model()

class ConcurrentTopUpAPITest(LiveServerTestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="concurrent", password="pass1234", credit=1000000)
        self.phone = PhoneNumber.objects.create(seller=self.user, number="09121234567",)

        # retrieve a token
        token_url = f"{self.live_server_url}/api/token/"
        r = requests.post(token_url, json={"username": "concurrent","password": "pass1234"})
        
        r.raise_for_status()
        self.token = r.json()["access"]
        self.headers = {"Authorization": f"Bearer {self.token}"}

    def _worker(self, amount, results, index):
        topup_url = f"{self.live_server_url}/api/credits/top-ups/"
        body = {"phone_number": self.phone.number, "amount": amount}
        try:
            resp = requests.post(topup_url, json=body, headers=self.headers)
            results[index] = resp.status_code
        except Exception as e:
            results[index] = f"EXC: {e}"

    def test_concurrent_topups(self):
        threads = []
        results = [None] * 1000
        for i in range(1000):
            t = threading.Thread(target=self._worker, args=(1000, results, i))
            threads.append(t)
            t.start()
            time.sleep(0.01)
        for t in threads:
            t.join()

        self.user.refresh_from_db()

        success_count = results.count(201)
        failure_count = len([r for r in results if r != 201])

        # Only 10 should succeed
        self.assertEqual(success_count, 1000, f"Expected 10 successes, got: {results}")
        self.assertEqual(self.user.credit, 0)

        # Rejected Threads
        self.assertEqual(failure_count, 0)
        

class ConnectionPoolingConcurrentTopUpAPITest(LiveServerTestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="concurrent", password="pass1234", credit=1000000)
        self.phone = PhoneNumber.objects.create(seller=self.user, number="09121234567")

        token_url = f"{self.live_server_url}/api/token/"
        r = requests.post(token_url, json={
            "username": "concurrent",
            "password": "pass1234"
        })
        r.raise_for_status()
        self.token = r.json()["access"]

        self.session = requests.Session()
        retry = Retry(
            total=3,
            backoff_factor=0.2,
            status_forcelist=[500, 502, 503, 504]
        )
        adapter = HTTPAdapter(
            pool_connections=200,
            pool_maxsize=1000,
            max_retries=retry
        )
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        self.headers = {"Authorization": f"Bearer {self.token}"}
        self.topup_url = f"{self.live_server_url}/api/credits/top-ups/"

    def _worker(self, amount, results, index):
        body = {"phone_number": self.phone.number, "amount": amount}
        try:
            resp = self.session.post(
                self.topup_url,
                json=body,
                headers=self.headers,
                timeout=10
            )
            results[index] = resp.status_code
        except Exception as e:
            results[index] = f"EXC: {type(e).__name__}"

    def test_concurrent_topups(self):
        num_requests = 50
        threads = []
        results = [None] * num_requests

        for i in range(num_requests):
            t = threading.Thread(
                target=self._worker,
                args=(20000, results, i)
            )
            threads.append(t)
            t.start()
            #time.sleep(0.005)

        for t in threads:
            t.join()

        self.user.refresh_from_db()

        success_count = results.count(201)
        failure_count = len([r for r in results if r != 201])

        self.assertEqual(success_count, num_requests, f"Expected {num_requests} successes, got: {results}")
        self.assertEqual(self.user.credit, 0, "Final credit should be zero")
        self.assertEqual(failure_count, 0, "There should be no failures")
