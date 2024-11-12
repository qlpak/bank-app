import unittest

from ..Konto import Konto, KontoOsobiste, KontoFirmowe

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

    def test_przelew_wychodzacy_successful(self):
        nadawca = Konto(self.imie, self.nazwisko, self.pesel)
        odbiorca = Konto("marek", "markowski", "10987654321")
        nadawca.saldo = 100
        wynik = nadawca.przelew_wychodzacy(50, odbiorca)
        self.assertEqual(wynik, True, "Przelew powinien się udać przy wystarczających środkach")
        self.assertEqual(nadawca.saldo, 50, "Saldo nadawcy powinno zmniejszyć się o kwotę przelewu")
        self.assertEqual(odbiorca.saldo, 50, "Saldo odbiorcy powinno zwiększyć się o kwotę przelewu")

    def test_przelew_wychodzacy_insufficient_funds(self):
        nadawca = Konto(self.imie, self.nazwisko, self.pesel)
        odbiorca = Konto("ania", "przymus", "10987654321")
        nadawca.saldo = 30
        wynik = nadawca.przelew_wychodzacy(50, odbiorca)
        self.assertEqual(wynik, False, "Przelew powinien zakończyć się niepowodzeniem przy niewystarczających środkach")
        self.assertEqual(nadawca.saldo, 30, "Saldo nadawcy powinno pozostać bez zmian")
        self.assertEqual(odbiorca.saldo, 0, "Saldo odbiorcy powinno pozostać bez zmian")

    def test_konto_firmowe_z_poprawnym_nip(self):
        konto_firmowe = KontoFirmowe("spolka", "1234567890")
        self.assertEqual(konto_firmowe.nip, "1234567890", "NIP powinien być zapisany poprawnie")

    def test_konto_firmowe_z_nieprawidlowym_nip(self):
        konto_firmowe = KontoFirmowe("firma x", "12345")
        self.assertEqual(konto_firmowe.nip, "Niepoprawny NIP!", "NIP niepoprawny")

    def test_przelew_ekspresowy_osobisty(self):
        nadawca = KontoOsobiste(self.imie, self.nazwisko, self.pesel)
        odbiorca = Konto("nikola", "lewandowska", "10987654321")
        nadawca.saldo = 10
        wynik = nadawca.przelew_ekspresowy(5, odbiorca)
        self.assertEqual(wynik, True, "Przelew ekspresowy powinien się powieść przy wystarczających środkach")
        self.assertEqual(nadawca.saldo, 4, "Saldo nadawcy powinno zostać pomniejszone o kwotę przelewu i opłatę")
        self.assertEqual(odbiorca.saldo, 5, "Saldo odbiorcy powinno zwiększyć się o kwotę przelewu")

    def test_przelew_ekspresowy_osobisty_insufficient_funds(self):
        nadawca = KontoOsobiste(self.imie, self.nazwisko, self.pesel)
        odbiorca = Konto("kto", "tam", "10987654321")
        nadawca.saldo = 5
        wynik = nadawca.przelew_ekspresowy(5, odbiorca)
        self.assertEqual(wynik, False, "Przelew ekspresowy powinien się nie powieść przy niewystarczających środkach")
        self.assertEqual(nadawca.saldo, 5, "Saldo nadawcy powinno pozostać bez zmian")
        self.assertEqual(odbiorca.saldo, 0, "Saldo odbiorcy powinno pozostać bez zmian")

    def test_przelew_ekspresowy_firmowy(self):
        nadawca = KontoFirmowe("pzu", "1234567890")
        odbiorca = Konto("ktos", "ciekawski", "10987654321")
        nadawca.saldo = 10
        wynik = nadawca.przelew_ekspresowy(5, odbiorca)
        self.assertEqual(wynik, True, "Przelew ekspresowy powinien się powieść przy wystarczających środkach")
        self.assertEqual(nadawca.saldo, 0, "Saldo nadawcy powinno zostać pomniejszone o kwotę przelewu i opłatę")
        self.assertEqual(odbiorca.saldo, 5, "Saldo odbiorcy powinno zwiększyć się o kwotę przelewu")

    def test_przelew_ekspresowy_firmowy_insufficient_funds(self):
        nadawca = KontoFirmowe("ccc", "1234567890")
        odbiorca = Konto("lukasz", "k", "10987654321")
        nadawca.saldo = 5
        wynik = nadawca.przelew_ekspresowy(5, odbiorca)
        self.assertEqual(wynik, False, "Przelew ekspresowy powinien się nie powieść przy niewystarczających środkach")
        self.assertEqual(nadawca.saldo, 5, "Saldo nadawcy powinno pozostać bez zmian")
        self.assertEqual(odbiorca.saldo, 0, "Saldo odbiorcy powinno pozostać bez zmian")

    def test_historia_przelewow(self):
        nadawca = KontoOsobiste("Kacperek", "Ziutowski", "12345678901")
        odbiorca = Konto("Coco", "Gofer", "10987654321")
        nadawca.saldo = 1000

        odbiorca.przelew_przychodzacy(500)
        self.assertEqual(odbiorca.historia, [500], "Historia powinna zawierać tylko 500")

        nadawca.przelew_wychodzacy(300, odbiorca)
        self.assertEqual(nadawca.historia, [-300], "Historia powinna zawierać -300")

        nadawca.przelew_ekspresowy(200, odbiorca)
        self.assertEqual(nadawca.historia, [-300, -200, -1], "Historia powinna zawierać kwoty -300, -200, -1")

    def test_kredyt_bez_histori(self):
        konto = KontoOsobiste(self.imie, self.nazwisko, self.pesel)
        wynik = konto.zaciagnij_kredyt(100)
        self.assertFalse(wynik, "kredyt nie udzielony przy brak hustorii")
        self.assertEqual(konto.saldo, 0, "saldo nie ma sie zmieniac")

    def test_kredyt_niewystarczajaca_historia(self):
        konto = KontoOsobiste(self.imie, self.nazwisko, self.pesel)
        konto.historia = [100, -50]
        wynik = konto.zaciagnij_kredyt(100)
        self.assertFalse(wynik, "kredyt nie uzielony bo nie wystarczajaca liczba transakcji")
        self.assertEqual(konto.saldo, 0, "saldo ma pozosatc bez zmian")

    def test_kredyt_warunek_a(self):
        konto = KontoOsobiste(self.imie, self.nazwisko, self.pesel)
        konto.historia = [100, 200, 300]
        wynik = konto.zaciagnij_kredyt(500)
        self.assertTrue(wynik, "kredyt udzielony przy trzech ostatnich wplatach")
        self.assertEqual(konto.saldo, 500, "saldo zwiekszone o kwote kredytu")

    def test_kredyt_warunek_b(self):
        konto = KontoOsobiste(self.imie, self.nazwisko, self.pesel)
        konto.historia = [150, 200, 100, -50, 250]
        wynik = konto.zaciagnij_kredyt(500)
        self.assertTrue(wynik, "kredyt powinien zosatc udzielon")
        self.assertEqual(konto.saldo, 500, "saldo ma byc zwiekszone o kwote kredytu")

    def test_kredyt_brak_warunkow(self):
        konto = KontoOsobiste(self.imie, self.nazwisko, self.pesel)
        konto.historia = [50, -50, 30, 40, -20]
        wynik = konto.zaciagnij_kredyt(200)
        self.assertFalse(wynik, "warunki niespelnione wiec kredyt nie udzielony")
        self.assertEqual(konto.saldo, 0, "saldo bez zmian")

