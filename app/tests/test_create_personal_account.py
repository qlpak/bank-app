import unittest
from parameterized import parameterized
from ..PersonalAccount import KontoOsobiste

class TestCreatePersonalAccount(unittest.TestCase):
    name = 'name'
    surname = 'surname'
    pesel = "12345678910"

    def setUp(self):
        self.konto = KontoOsobiste(self.name, self.surname, self.pesel)

    def test_tworzenie_konta(self):
        self.assertEqual(self.konto.name, self.name, "Imię nie zostało zapisane!")
        self.assertEqual(self.konto.surname, self.surname, "Nazwisko nie zostało zapisane!")
        self.assertEqual(self.konto.saldo, 0, "Saldo nie jest zerowe!")
        self.assertEqual(self.konto.pesel, self.pesel, "PESEL nie został zapisany")

    @parameterized.expand([
        ('123', "niepoprawny pesel", "PESEL nie został zapisany jako niepoprawny"),
    ])
    def test_pesel_krotki(self, pesel, expected_pesel, message):
        konto = KontoOsobiste(self.name, self.surname, pesel)
        self.assertEqual(konto.pesel, expected_pesel, message)

    @parameterized.expand([
        ("PROM_ddddd34", 0, "Kod rabatowy niepoprawny - saldo powinno pozostać zerowe"),
        ("PROM_xdf", 50, "Niepoprawny kod rabatowy nie powinien dodawać salda"),
        ("invalif", 0, "Poprawny kod rabatowy powinien dodać 50 zł do salda"),
    ])
    def test_kod_rabatowy(self, kod, expected_saldo, message):
        konto = KontoOsobiste(self.name, self.surname, self.pesel, kod)
        self.assertEqual(konto.saldo, expected_saldo, message)

    @parameterized.expand([
        ('60010212305', 0, "Osoba, która urodziła się przed 1961, nie powinna dostać 50 zł"),
        ('85010452345', 50, "Osoba, która urodziła się po 1960, powinna dostać 50 zł"),
    ])
    def test_pesel_wiek_z_kodem_rabatowym(self, pesel, expected_saldo, message):
        konto = KontoOsobiste(self.name, self.surname, pesel, "PROM_abc")
        self.assertEqual(konto.saldo, expected_saldo, message)
