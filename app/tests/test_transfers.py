import unittest
from parameterized import parameterized
from ..Account import Account
from ..PersonalAccount import PersonalAccount
from ..CompanyAccount import CompanyAccount

class TestTransfers(unittest.TestCase):
    @parameterized.expand([
        (100, 50, True, 50, 50, "Przelew powinien się udać przy wystarczających środkach"),
        (30, 50, False, 30, 0, "Przelew powinien zakończyć się niepowodzeniem przy niewystarczających środkach")
    ])
    def test_przelew_wychodzacy(self, saldo_nadawcy, kwota, expected_result, expected_saldo_nadawcy, expected_saldo_odbiorcy, message):
        nadawca = PersonalAccount("Jan", "Kowalski", "12345678901")
        odbiorca = PersonalAccount("Marek", "Markowski", "10987654321")
        nadawca.saldo = saldo_nadawcy
        wynik = nadawca.przelew_wychodzacy(kwota, odbiorca)
        self.assertEqual(wynik, expected_result, message)
        self.assertEqual(nadawca.saldo, expected_saldo_nadawcy, "Saldo nadawcy powinno zmniejszyć się o kwotę przelewu")
        self.assertEqual(odbiorca.saldo, expected_saldo_odbiorcy, "Saldo odbiorcy powinno zwiększyć się o kwotę przelewu")

    @parameterized.expand([
        (10, 5, 1, True, 4, 5, "Przelew ekspresowy powinien się powieść przy wystarczających środkach"),
        (5, 5, 1, False, 5, 0, "Przelew ekspresowy powinien się nie powieść przy niewystarczających środkach"),
    ])
    def test_przelew_ekspresowy_osobisty(self, saldo, kwota, oplata, expected_result, saldo_po, saldo_odbiorcy, message):
        nadawca = PersonalAccount("Jan", "Kowalski", "12345678901")
        odbiorca = PersonalAccount("Nikola", "Lewandowska", "10987654321")
        nadawca.saldo = saldo
        wynik = nadawca.przelew_ekspresowy(kwota, odbiorca)
        self.assertEqual(wynik, expected_result, message)
        self.assertEqual(nadawca.saldo, saldo_po, "Saldo nadawcy po przelewie ekspresowym nie jest zgodne z oczekiwanym")
        self.assertEqual(odbiorca.saldo, saldo_odbiorcy, "Saldo odbiorcy po przelewie ekspresowym nie jest zgodne z oczekiwanym")

    @parameterized.expand([
        (10, 5, 5, True, 0, 5, "Przelew ekspresowy powinien się powieść przy wystarczających środkach"),
        (5, 5, 5, False, 5, 0, "Przelew ekspresowy powinien się nie powieść przy niewystarczających środkach"),
    ])
    def test_przelew_ekspresowy_firmowy(self, saldo, kwota, oplata, expected_result, saldo_po, saldo_odbiorcy, message):
        nadawca = CompanyAccount("PZU", "1234567890")
        odbiorca = Account("Ktos", "Ciekawski", "10987654321")
        nadawca.saldo = saldo
        wynik = nadawca.przelew_ekspresowy(kwota, odbiorca)
        self.assertEqual(wynik, expected_result, message)
        self.assertEqual(nadawca.saldo, saldo_po, "Saldo nadawcy po przelewie ekspresowym nie jest zgodne z oczekiwanym")
        self.assertEqual(odbiorca.saldo, saldo_odbiorcy, "Saldo odbiorcy po przelewie ekspresowym nie jest zgodne z oczekiwanym")

    def test_historia_przelewow(self):
        nadawca = PersonalAccount("Kacperek", "Ziutowski", "12345678901")
        odbiorca = Account("Coco", "Gofer", "10987654321")
        nadawca.saldo = 1000

        odbiorca.przelew_przychodzacy(500)
        self.assertEqual(odbiorca.historia, [500], "Historia powinna zawierać tylko 500")

        nadawca.przelew_wychodzacy(300, odbiorca)
        self.assertEqual(nadawca.historia, [-300], "Historia powinna zawierać -300")

        nadawca.przelew_ekspresowy(200, odbiorca)
        self.assertEqual(nadawca.historia, [-300, -200, -1], "Historia powinna zawierać kwoty -300, -200, -1")
