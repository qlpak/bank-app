import unittest
from parameterized import parameterized
from ..PersonalAccount import KontoOsobiste
from ..AccountRegistry import AccountRegistry

class TestRegistry(unittest.TestCase):
    imie = 'Miroslaw'
    nazwisko = 'Nowak'
    pesel = '12345678910'
    pesel_00 = "88776655400"
    pesel_75 = '12674589775'
    pesel_not = '99999999999'

    @classmethod
    def setUpClass(cls):
        cls.konto = KontoOsobiste(cls.imie, cls.nazwisko, cls.pesel)
        cls.konto_00 = KontoOsobiste(cls.imie, cls.nazwisko, cls.pesel_00)
        cls.konto_75 = KontoOsobiste(cls.imie, cls.nazwisko, cls.pesel_75)

    def setUp(self):
        AccountRegistry.registry = []

    def test_add_acc(self):
        AccountRegistry.add_account(self.konto)
        self.assertEqual(AccountRegistry.get_accounts_count(), 1, "Błędna ilość kont w rejestrze")

    @parameterized.expand([
        ("konto_00", 1, "Błędna ilość kont w rejestrze"),
        ("konto_75", 1, "Błędna ilość kont w rejestrze"),
        ("konto_00 i konto_75", 2, "Błędna ilość kont w rejestrze")
    ])
    def test_add_multiple_accounts(self, test_name, expected_count, message):
        if expected_count == 1:
            AccountRegistry.add_account(self.konto_00)
        elif expected_count == 2:
            AccountRegistry.add_account(self.konto_00)
            AccountRegistry.add_account(self.konto_75)
        self.assertEqual(AccountRegistry.get_accounts_count(), expected_count, message)

    @parameterized.expand([
        ("konto", "12345678910", "Błędne konto znalezione po PESEL"),
        ("konto_00", "88776655400", "Błędne konto znalezione po PESEL"),
        ("konto_75", "12674589775", "Błędne konto znalezione po PESEL")
    ])
    def test_search_by_pesel(self, test_name, pesel, message):
        if pesel == self.pesel:
            konto = self.konto
        elif pesel == self.pesel_00:
            konto = self.konto_00
        elif pesel == self.pesel_75:
            konto = self.konto_75

        AccountRegistry.add_account(konto)
        result = AccountRegistry.search_by_pesel(pesel)
        self.assertEqual(result, konto, message)

    def test_search_by_pesel_not_found(self):
        AccountRegistry.add_account(self.konto)
        AccountRegistry.add_account(self.konto_00)

        result = AccountRegistry.search_by_pesel(self.pesel_not)
        self.assertEqual(result, None, "Znaleziono konto, którego nie ma w rejestrze")
