import unittest
from unittest.mock import patch
from ..CompanyAccount import CompanyAccount

class TestValidateNip(unittest.TestCase):
    @patch('requests.get')
    def test_valid_nip(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = "Valid NIP"
        konto = CompanyAccount("Firma A", "1234567890")
        self.assertEqual(konto.nip, "1234567890")

    @patch('requests.get')
    def test_invalid_nip(self, mock_get):
        mock_get.return_value.status_code = 404
        mock_get.return_value.text = "Company not registered!!"
        konto = None
        try:
            konto = CompanyAccount("Firma B", "1234567890")
        except ValueError as e:
            self.assertEqual(str(e), "Company not registered!!")
        self.assertEqual(konto, None)

    @patch('requests.get')
    def test_short_nip(self, mock_get):
        konto = CompanyAccount("Firma C", "12345")
        self.assertEqual(konto.nip, "Niepoprawny NIP!")

    @patch('requests.get')
    def test_api_failure(self, mock_get):
        mock_get.side_effect = Exception("API error occurred while validating NIP")
        konto = None
        try:
            konto = CompanyAccount("Firma D", "1234567890")
        except ValueError as e:
            self.assertEqual(str(e), "API error occurred while validating NIP")
        self.assertEqual(konto, None)
