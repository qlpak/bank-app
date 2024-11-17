import unittest
from parameterized import parameterized
from ..PersonalAccount import KontoOsobiste

class TestPersonalLoan(unittest.TestCase):
    @parameterized.expand([
        ([], 100, False, "Kredyt nie udzielony przy braku historii"),
        ([100, -50], 100, False, "Kredyt nie udzielony przy niewystarczającej liczbie transakcji"),
        ([100, 200, 300], 500, True, "Kredyt udzielony przy trzech ostatnich wpłatach"),
        ([150, 200, 100, -50, 250], 500, True, "Kredyt powinien zostać udzielony przy spełnionym warunku b"),
        ([50, -50, 30, 40, -20], 200, False, "Warunki niespełnione - kredyt nie udzielony")
    ])
    def test_zaciagnij_kredyt_osobisty(self, historia, kwota, expected, message):
        konto = KontoOsobiste("Jan", "Kowalski", "12345678901")
        konto.historia = historia
        wynik = konto.zaciagnij_kredyt(kwota)
        self.assertEqual(wynik, expected, message)

