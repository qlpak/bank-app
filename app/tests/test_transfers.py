import unittest
from parameterized import parameterized
from ..Konto import Konto
from ..PersonalAccount import KontoOsobiste

class TestTransfers(unittest.TestCase):
    def setUp(self):
        self.nadawca = KontoOsobiste("nadawca", "nazwisko", "12345678910")
        self.odbiorca = Konto("odbiorca", "nazwisko", "10987654321")

    @parameterized.expand([
        (100, 50, True, 50, 50, "Przelew powinien się udać przy wystarczających środkach"),
        (30, 50, False, 30, 0, "Przelew powinien zakończyć się niepowodzeniem przy niewystarczających środkach")
    ])
    def test_przelew_wychodzacy(self, saldo_nadawcy, kwota, expected_result, expected_saldo_nadawcy, expected_saldo_odbiorcy, message):
        self.nadawca.saldo = saldo_nadawcy
        wynik = self.nadawca.przelew_wychodzacy(kwota, self.odbiorca)
        self.assertEqual(wynik, expected_result, message)
        self.assertEqual(self.nadawca.saldo, expected_saldo_nadawcy, "Saldo nadawcy powinno zmniejszyć się o kwotę przelewu")
        self.assertEqual(self.odbiorca.saldo, expected_saldo_odbiorcy, "Saldo odbiorcy powinno zwiększyć się o kwotę przelewu")

    def test_historia_przelewow(self):
        self.nadawca.saldo = 1000
        self.odbiorca.przelew_przychodzacy(500)
        self.assertEqual(self.odbiorca.historia, [500], "Historia powinna zawierać tylko 500")

        self.nadawca.przelew_wychodzacy(300, self.odbiorca)
        self.assertEqual(self.nadawca.historia, [-300], "Historia powinna zawierać -300")

        self.nadawca.przelew_ekspresowy(200, self.odbiorca)
        self.assertEqual(self.nadawca.historia, [-300, -200, -1], "Historia powinna zawierać kwoty -300, -200, -1")