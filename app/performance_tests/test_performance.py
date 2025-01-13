import unittest
import requests
from time import time

class TestPerformance(unittest.TestCase):
    base_url = "http://127.0.0.1:5000/api/accounts"

    def test_create_and_delete_accounts(self):
        for i in range(100):
            pesel = f"{90000000000 + i}"
            account_data = {
                "name": "Test",
                "surname": "Performance",
                "pesel": pesel
            }
            start = time()
            response = requests.post(self.base_url, json=account_data, timeout=0.5)
            duration = time() - start
            self.assertEqual(response.status_code, 201, f"Failed to create account {pesel}")
            self.assertEqual(duration <= 0.5, True, f"Response time exceeded 0.5s for account creation {pesel}")

            start = time()
            response = requests.delete(f"{self.base_url}/{pesel}", timeout=0.5)
            duration = time() - start
            self.assertEqual(response.status_code, 200, f"Failed to delete account {pesel}")
            self.assertEqual(duration <= 0.5, True, f"Response time exceeded 0.5s for account deletion {pesel}")

    def test_incoming_transfers(self):
        pesel = "12345678901"
        account_data = {"name": "Test", "surname": "Performance", "pesel": pesel}
        requests.post(self.base_url, json=account_data)

        for i in range(100):
            transfer_data = {"type": "incoming", "amount": 10}
            start = time()
            response = requests.post(f"{self.base_url}/{pesel}/transfer", json=transfer_data, timeout=0.5)
            duration = time() - start
            self.assertEqual(response.status_code, 200, f"Failed to perform transfer {i + 1}")
            self.assertEqual(duration <= 0.5, True, f"Response time exceeded 0.5s for transfer {i + 1}")

        account_response = requests.get(f"{self.base_url}/{pesel}")
        self.assertEqual(account_response.status_code, 200, "Failed to fetch account details")
        self.assertEqual(account_response.json()["saldo"], 1000, "Final saldo mismatch")
