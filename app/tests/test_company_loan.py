import unittest
from parameterized import parameterized
from ..CompanyAccount import KontoFirmowe

class TestCompanyLoan(unittest.TestCase):
    @parameterized.expand([
        (4000, 1000, [-1775], True, "kredyt ok oba warunki spelnione"),
        (3000, 2000, [-1775, -500], False, "kredyt przyznany"),
        (500, 300, [], False, "kredyt nie ok, oba warunki nie spelnione"),
        (2000, 1500, [-1775], False, "kredyt nie ok, saldo zle"),
        (4000, 2000, [-100, -1775], True, "kredyt nie ok, brak kwoty 1775"),
])
    def test_zaciagnij_kredyt_firmowy(self, saldo, kwota, historia, expected, message):
        konto_firmowe = KontoFirmowe("salon pieknych fryzur", "1234567890")
        konto_firmowe.saldo = saldo
        konto_firmowe.historia = historia
        wynik = konto_firmowe.zaciagnij_kredyt(kwota)
        self.assertEqual(wynik, expected, message)