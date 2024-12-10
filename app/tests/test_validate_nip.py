import unittest
from unittest.mock import patch
from ..CompanyAccount import KontoFirmowe

class TestValidateNip(unittest.TestCase):
    @patch('requests.get')
    def test_valid_nip(self, mock_get):
        mock_get.return_value.status_code = 200
        KontoFirmowe("Firma A", "1234567890")

    @patch('requests.get')
    def test_invalid_nip(self, mock_get):
        mock_get.return_value.status_code = 404
        with self.assertRaises(ValueError):
            KontoFirmowe("Firma B", "1234567890")

    @patch('requests.get')
    def test_short_nip(self, mock_get):
        konto = KontoFirmowe("Firma C", "12345")
        self.assertEqual(konto.nip, "Niepoprawny NIP!")
        mock_get.assert_not_called()

    @patch('requests.get')
    def test_api_failure(self, mock_get):
        mock_get.side_effect = Exception("API error")
        with self.assertRaises(ValueError):
            KontoFirmowe("Firma D", "1234567890")
