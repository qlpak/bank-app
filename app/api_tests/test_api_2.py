import unittest
import requests

url = "http://127.0.0.1:5000/api/accounts"

class TestUniquePesel(unittest.TestCase):

    def setUp(self):
        requests.delete(f"{url}/all")

    def test_create_account_unique_pesel(self):
        data = {
            "imie": "Gosia",
            "nazwisko": "Goski",
            "pesel": "12345678901"
        }
        response = requests.post(f"{url}/unique", json=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"message": "Account created"})

    def test_create_account_duplicate_pesel(self):
        data = {
            "imie": "Jan",
            "nazwisko": "jakiś",
            "pesel": "12345678901"
        }
        requests.post(f"{url}/unique", json=data)

        response = requests.post(f"{url}/unique", json=data)
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.json(), {"message": "PESEL already exists"})

    def test_create_multiple_accounts_unique_pesel(self):
        accounts = [
            {"imie": "Jan", "nazwisko": "jakis", "pesel": "12345678901"},
            {"imie": "Anna", "nazwisko": "dentystka", "pesel": "98765432109"}
        ]
        for account in accounts:
            response = requests.post(f"{url}/unique", json=account)
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.json(), {"message": "Account created"})

    def tearDown(self):
        requests.delete(f"{url}/all")
