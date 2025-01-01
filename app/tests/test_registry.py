import unittest
import os
import json
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
        self.konto = KontoOsobiste(self.imie, self.nazwisko, self.pesel)

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

    @parameterized.expand([
        ("konto istnieje", "12345678910", "konto nie zostalo usuniete", 0),
        ("konto nie istnieje", "99999999999", "zly wynik", 1)
    ])
    def test_delete_account_by_pesel(self, test_name, pesel, message, expected_count):
        AccountRegistry.add_account(self.konto)
        AccountRegistry.delete_account_by_pesel(pesel)
        self.assertEqual(AccountRegistry.get_accounts_count(), expected_count, message)

    @parameterized.expand([
        ("aktualizacja pełna", "12345678910", {"imie": "andrew", "nazwisko": "broski"}, "andrew", "broski"),
        ("aktualizacja częściowa", "12345678910", {"imie": "andrew"}, "andrew", "Nowak"),
        ("konto nie istnieje", "99999999999", {"imie": "Test"}, None, None)
    ])
    def test_update_account(self, test_name, pesel, updates, expected_imie, expected_nazwisko):
        AccountRegistry.add_account(self.konto)
        AccountRegistry.update_account(pesel, **updates)
        updated_account = AccountRegistry.search_by_pesel(pesel)
        if updated_account is None:
            self.assertEqual(updated_account, None, "konto ktore nie istnieje zostalo updateowane")
        else:
            self.assertEqual(updated_account.imie, expected_imie, "imie nie zostalo zupdateowane")
            self.assertEqual(updated_account.nazwisko, expected_nazwisko, "nazwisko nie zostalo zupdateowane")

    @parameterized.expand([
        ("brak kont", [], 0, "rejestr mial byc pusty"),
        ("jedno konto", ["konto"], 0, "rejest mial byc pusty"),
        ("trzy konta", ["konto", "konto_00", "konto_75"], 0, "rejest mial byc pusty")
    ])
    def test_clear_registry(self, test_name, accounts_to_add, expected_count, message):
        for account_name in accounts_to_add:
            if account_name == "konto":
                AccountRegistry.add_account(self.konto)
            elif account_name == "konto_00":
                AccountRegistry.add_account(self.konto_00)
            elif account_name == "konto_75":
                AccountRegistry.add_account(self.konto_75)

        AccountRegistry.clear_registry()
        self.assertEqual(AccountRegistry.get_accounts_count(), expected_count, message)


    @parameterized.expand([
        ("unikalny pesel", "12345678910", True, "pesel mial być unikalny"),
        ("zduplikowany PESEL", "12345678910", False, "pesel nie powinien być unikalny"),
        ("unikalny PESEL - nowy", "99999999999", True, "nowy pesel mial być unikalny")
    ])
    def test_is_pesel_unique(self, test_name, pesel, expected_result, message):
        if not expected_result:
            AccountRegistry.add_account(self.konto)

        result = AccountRegistry.is_pesel_unique(pesel)
        self.assertEqual(result, expected_result, message)

    def tearDown(self):
        if os.path.exists("test_backup.json"):
            os.remove("test_backup.json")

    def test_dump_backup(self):
        AccountRegistry.add_account(self.konto)
        AccountRegistry.dump_backup("test_backup.json")
        with open("test_backup.json", "r") as file:
            data = json.load(file)
        self.assertEqual(len(data), 1, "backup nie zawiera odpowiedniej liczby kont")

    def test_load_backup(self):
        AccountRegistry.add_account(self.konto)
        AccountRegistry.dump_backup("test_backup.json")
        AccountRegistry.clear_registry()
        AccountRegistry.load_backup("test_backup.json")
        self.assertEqual(AccountRegistry.get_accounts_count(), 1, "konta nie zostały poprawnie załadowane z backupu")