import unittest
from ..Konto import Konto, KontoOsobiste, KontoFirmowe
from parameterized import parameterized

class TestCreateBankAccount(unittest.TestCase):
    imie = 'imie'
    nazwisko = 'nazwisko'
    pesel = "12345678910"

    def setUp(self):
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
        konto = Konto(self.imie, self.nazwisko, pesel)
        self.assertEqual(konto.pesel, expected_pesel, message)

    @parameterized.expand([
        ("PROM_ddddd34", 0, "Pesel nie zostal zapisany"),
        ("PROM_xdf", 50, "Saldo nie zostalo dodane poprawnie dodane"),
        ("INVALID", 0, "Kod rabatowy zle dodaje saldo"),
    ])
    def test_kod_rabatowy(self, kod, expected_saldo, message):
        konto = Konto(self.imie, self.nazwisko, self.pesel, kod)
        self.assertEqual(konto.saldo, expected_saldo, message)

    @parameterized.expand([
        ('60010212305', 0, "osoba która urodzila sie przed 1961 nie powinna dostać 50 zł"),
        ('85010452345', 50, "Osoba która urodzila sie po 1960 powinna dostać 50 zł"),
    ])
    def test_pesel_wiek_z_kodem_rabatowym(self, pesel, expected_saldo, message):
        konto = Konto(self.imie, self.nazwisko, pesel, "PROM_abc")
        self.assertEqual(konto.saldo, expected_saldo, message)

    @parameterized.expand([
        (100, 50, True, 50, 50, "Przelew powinien się udać przy wystarczających środkach"),
        (30, 50, False, 30, 0, "Przelew powinien zakończyć się niepowodzeniem przy niewystarczających środkach")
    ])
    def test_przelew_wychodzacy(self, saldo_nadawcy, kwota, expected_result, expected_saldo_nadawcy, expected_saldo_odbiorcy, message):
        nadawca = Konto(self.imie, self.nazwisko, self.pesel)
        odbiorca = Konto("marek", "markowski", "10987654321")
        nadawca.saldo = saldo_nadawcy
        wynik = nadawca.przelew_wychodzacy(kwota, odbiorca)
        self.assertEqual(wynik, expected_result, message)
        self.assertEqual(nadawca.saldo, expected_saldo_nadawcy, "Saldo nadawcy powinno zmniejszyć się o kwotę przelewu")
        self.assertEqual(odbiorca.saldo, expected_saldo_odbiorcy, "Saldo odbiorcy powinno zwiększyć się o kwotę przelewu")

    @parameterized.expand([
        ("spolka", "1234567890", "1234567890", "NIP powinien być zapisany poprawnie"),
        ("firma x", "12345", "Niepoprawny NIP!", "NIP niepoprawny")
    ])
    def test_konto_firmowe_nip(self, nazwa_firmy, nip, expected_nip, message):
        konto_firmowe = KontoFirmowe(nazwa_firmy, nip)
        self.assertEqual(konto_firmowe.nip, expected_nip, message)

    @parameterized.expand([
        (10, 5, 1, True, 4, 5, "Przelew ekspresowy powinien się powieść przy wystarczających środkach"),
        (5, 5, 1, False, 5, 0, "Przelew ekspresowy powinien się nie powieść przy niewystarczających środkach"),
    ])
    def test_przelew_ekspresowy_osobisty(self, saldo, kwota, oplata, expected_result, saldo_po, saldo_odbiorcy, message):
        nadawca = KontoOsobiste(self.imie, self.nazwisko, self.pesel)
        odbiorca = Konto("nikola", "lewandowska", "10987654321")
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
        nadawca = KontoFirmowe("pzu", "1234567890")
        odbiorca = Konto("ktos", "ciekawski", "10987654321")
        nadawca.saldo = saldo
        wynik = nadawca.przelew_ekspresowy(kwota, odbiorca)
        self.assertEqual(wynik, expected_result, message)
        self.assertEqual(nadawca.saldo, saldo_po, "Saldo nadawcy po przelewie ekspresowym nie jest zgodne z oczekiwanym")
        self.assertEqual(odbiorca.saldo, saldo_odbiorcy, "Saldo odbiorcy po przelewie ekspresowym nie jest zgodne z oczekiwanym")

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

    @parameterized.expand([
        ([], 100, False, "kredyt nie udzielony przy brak historii"),
        ([100, -50], 100, False, "kredyt nie udzielony przy niewystarczającej liczbie transakcji"),
        ([100, 200, 300], 500, True, "kredyt udzielony przy trzech ostatnich wplatach"),
        ([150, 200, 100, -50, 250], 500, True, "kredyt powinien zostać udzielony przy spełnionym warunku b"),
        ([50, -50, 30, 40, -20], 200, False, "warunki niespełnione - kredyt nie udzielony")
    ])
    def test_zaciagnij_kredyt(self, historia, kwota, expected, message):
        konto = KontoOsobiste(self.imie, self.nazwisko, self.pesel)
        konto.historia = historia
        wynik = konto.zaciagnij_kredyt(kwota)
        self.assertEqual(wynik, expected, message)

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