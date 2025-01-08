import unittest
import requests

class TestCRUD(unittest.TestCase):
    base_url = "http://127.0.0.1:5000/api/accounts"
    body = {
        "name": "James",
        "surname": "Hetfield",
        "pesel": "89092909825"
    }

    def tearDown(self):
        response = requests.delete(f"{self.base_url}/all")

    def test_create_account(self):
        response = requests.post(self.base_url, json=self.body)
        self.assertEqual(response.status_code, 201, "wrong status code")

    def test_get_account_by_pesel(self):
        requests.post(self.base_url, json=self.body)
        pesel = self.body["pesel"]
        response = requests.get(f"{self.base_url}/{pesel}")
        self.assertEqual(response.status_code, 200, "wrong status code")
        self.assertEqual(response.json()["name"], self.body["name"])
        self.assertEqual(response.json()["surname"], self.body["surname"])
        self.assertEqual(response.json()["pesel"], self.body["pesel"])
        self.assertEqual(response.json()["saldo"], 0)

    def test_get_account_not_found(self):
        pesel = "99999999999"
        response = requests.get(f"{self.base_url}/{pesel}")
        self.assertEqual(response.status_code, 404, "wrong status code")
        self.assertEqual(response.json()["message"], "konta brak")

    def test_update_account(self):
        requests.post(self.base_url, json=self.body)
        pesel = self.body["pesel"]
        update_body = {"name": "kacpi"}
        response = requests.patch(f"{self.base_url}/{pesel}", json=update_body)
        self.assertEqual(response.status_code, 200, "wrong status code")

        updated_account = requests.get(f"{self.base_url}/{pesel}")
        self.assertEqual(updated_account.json()["name"], "kacpi")
        self.assertEqual(updated_account.json()["surname"], self.body["surname"])

    def test_delete_account(self):
        requests.post(self.base_url, json=self.body)
        pesel = self.body["pesel"]
        requests.delete(f"{self.base_url}/{pesel}")

        not_found = requests.get(f"{self.base_url}/{pesel}")
        self.assertEqual(not_found.status_code, 404, "konto wciaz istnieje a nie powinno po usunieciu")

    def test_get_account_count(self):
        requests.post(self.base_url, json=self.body)
        response = requests.get(f"{self.base_url}/count")
        self.assertEqual(response.status_code, 200, "wrong status code")
        self.assertEqual(response.json()["count"], 1)
