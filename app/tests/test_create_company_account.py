import unittest
from parameterized import parameterized
from ..CompanyAccount import KontoFirmowe

class TestCreateCompanyAccount(unittest.TestCase):
    @parameterized.expand([
        ("spolka", "1234567890", "1234567890", "NIP powinien być zapisany poprawnie"),
        ("firma x", "12345", "Niepoprawny NIP!", "NIP niepoprawny")
])
    def test_konto_firmowe_nip(self, nazwa_firmy, nip, expected_nip, message):
        konto_firmowe = KontoFirmowe(nazwa_firmy, nip)
        self.assertEqual(konto_firmowe.nip, expected_nip, message)