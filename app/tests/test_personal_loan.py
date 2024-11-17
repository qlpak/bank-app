import unittest
from parameterized import parameterized
from ..PersonalAccount import KontoOsobiste

class TestPersonalLoan(unittest.TestCase):
    def setUp(self):
        self.konto_osobiste = KontoOsobiste("imie", "nazwisko", "12345678910")

    @parameterized.expand([
        ([], 100, False, "kredyt nie udzielony przy brak historii"),
        ([100, -50], 100, False, "kredyt nie udzielony przy niewystarczającej liczbie transakcji"),
        ([100, 200, 300], 500, True, "kredyt udzielony przy trzech ostatnich wplatach"),
        ([150, 200, 100, -50, 250], 500, True, "kredyt powinien zostać udzielony przy spełnionym warunku b"),
        ([50, -50, 30, 40, -20], 200, False, "warunki niespełnione - kredyt nie udzielony")
    ])
    def test_zaciagnij_kredyt(self, historia, kwota, expected, message):
        self.konto_osobiste.historia = historia
        wynik = self.konto_osobiste.zaciagnij_kredyt(kwota)
        self.assertEqual(wynik, expected, message)