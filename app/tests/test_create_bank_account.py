import unittest

from ..Konto import Konto

class TestCreateBankAccount(unittest.TestCase):
    imie = 'imie'
    nazwisko = 'nazwisko'
    pesel = "12345678910"

    def test_tworzenie_konta(self):
        pierwsze_konto = Konto(self.imie, self.nazwisko, self.pesel)
        self.assertEqual(pierwsze_konto.imie, self.imie, "Imie nie zostało zapisane!")
        self.assertEqual(pierwsze_konto.nazwisko, self.nazwisko, "Nazwisko nie zostało zapisane!")
        self.assertEqual(pierwsze_konto.saldo, 0, "Saldo nie jest zerowe!")
        self.assertEqual(pierwsze_konto.pesel, self.pesel, "pesel nie został zapisany" )

    def test_pesel_krotki(self):
        krotki_pesel = '123'
        konto = Konto(self.imie, self.nazwisko, krotki_pesel)
        self.assertEqual(konto.pesel, "niepoprawny pesel", "pesel nie zostal zapisany")

    def test_kod_suffix(self):
        konto  =Konto(self.imie, self.nazwisko, self.pesel, "PROM_ddddd34")
        self.assertEqual(konto.saldo, 0, "Pesel nie zostal zapisany")

    def test_kod_rabatowy_saldo_plus(self):
        konto = Konto(self.imie, self.nazwisko, self.pesel, "PROM_xdf")
        self.assertEqual(konto.saldo, 50, "Saldo nie zostalo dodane poprawnie dodane")

    def test_kod_rabatowy_zly(self):
        konto = Konto(self.imie, self.nazwisko, self.pesel, "INVALID")
        self.assertEqual(konto.saldo, 0, "Kod rabatowy zle dodaje saldo")

    def test_pesel_senior_bez_kodu_rabatowego(self):
        pesel_senior = '60010212305'
        konto = Konto(self.imie, self.nazwisko, pesel_senior, "PROM_xyz")
        self.assertEqual(konto.saldo, 0, "osoba która urodzila sie przed 1961 nie powinna dostać 50 zł")

    def test_pesel_mlody_z_kodem_rabatowym(self):
        pesel_mlody = '85010452345'
        konto = Konto(self.imie, self.nazwisko, pesel_mlody, "PROM_abc")
        self.assertEqual(konto.saldo, 50, "Osoba która urodzila sie po 1960 powinna dostać 50 zł")
    #     #tutaj proszę dodawać nowe testy
