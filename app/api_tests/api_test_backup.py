import unittest
import requests

class TestBackupAPI(unittest.TestCase):
    base_url = "http://127.0.0.1:5000/api/accounts"
    backup_url = f"{base_url}/backup"
    sample_account = {
        "imie": "Jan",
        "nazwisko": "Kowalski",
        "pesel": "12345678901"
    }

    def setUp(self):
        requests.delete(f"{self.base_url}/all")

    def tearDown(self):
        requests.delete(f"{self.base_url}/all")

    def test_dump_backup(self):
        requests.post(self.base_url, json=self.sample_account)
        response = requests.post(f"{self.backup_url}/dump")
        self.assertEqual(response.status_code, 200, "backup dump failed")
        self.assertIn("backup saved", response.json().get("message"))

    def test_load_backup(self):
        requests.post(self.base_url, json=self.sample_account)
        requests.post(f"{self.backup_url}/dump")
        requests.delete(f"{self.base_url}/all")
        response = requests.post(f"{self.backup_url}/load")
        self.assertEqual(response.status_code, 200, "backup load failed")
        restored_account = requests.get(f"{self.base_url}/{self.sample_account['pesel']}")
        self.assertEqual(restored_account.status_code, 200, "restored account not found")
        self.assertEqual(restored_account.json()["imie"], self.sample_account["imie"])

    def test_load_backup_file_not_found(self):
        response = requests.post(f"{self.backup_url}/load")
        self.assertEqual(response.status_code, 404, "expected file not found error")
        self.assertEqual(response.json()["message"], "backup file not found")
