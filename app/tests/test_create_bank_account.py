import unittest
from parameterized import parameterized
from ..PersonalAccount import KontoOsobiste

class TestCreateBankAccount(unittest.TestCase):
    def setUp(self):
        self.imie = "imie"
        self.nazwisko = "nazwisko"
        self.pesel = "12345678910"
        self.konto = KontoOsobiste(self.imie, self.nazwisko, self.pesel)

    def test_tworzenie_konta(self):
        self.assertEqual(self.konto.imie, self.imie, "Imię nie zostało zapisane!")
        self.assertEqual(self.konto.nazwisko, self.nazwisko, "Nazwisko nie zostało zapisane!")
        self.assertEqual(self.konto.saldo, 0, "Saldo nie jest zerowe!")
        self.assertEqual(self.konto.pesel, self.pesel, "PESEL nie został zapisany")

    @parameterized.expand([
        ('123', "niepoprawny pesel", "pesel nie zostal zapisany"),
    ])
    def test_pesel_krotki(self, pesel, expected_pesel, message):
        konto = KontoOsobiste(self.imie, self.nazwisko, pesel)
        self.assertEqual(konto.pesel, expected_pesel, message)

    @parameterized.expand([
        ("PROM_ddddd34", 0, "Pesel nie zostal zapisany"),
        ("PROM_xdf", 50, "Saldo nie zostalo dodane poprawnie dodane"),
        ("INVALID", 0, "Kod rabatowy zle dodaje saldo"),
    ])
    def test_kod_rabatowy(self, kod, expected_saldo, message):
        konto = KontoOsobiste(self.imie, self.nazwisko, self.pesel, kod)
        self.assertEqual(konto.saldo, expected_saldo, message)

    @parameterized.expand([
        ('60010212305', 0, "osoba która urodzila sie przed 1961 nie powinna dostać 50 zł"),
        ('85010452345', 50, "Osoba która urodzila sie po 1960 powinna dostać 50 zł"),
    ])
    def test_pesel_wiek_z_kodem_rabatowym(self, pesel, expected_saldo, message):
        konto = KontoOsobiste(self.imie, self.nazwisko, pesel, "PROM_abc")
        self.assertEqual(konto.saldo, expected_saldo, message)
