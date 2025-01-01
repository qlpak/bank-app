import json
from .PersonalAccount import KontoOsobiste

class AccountRegistry:
    registry = []

    @classmethod
    def add_account(cls, account):
        cls.registry.append(account)

    @classmethod
    def get_accounts_count(cls):
        return len(cls.registry)

    @classmethod
    def search_by_pesel(cls, pesel):
        for account in cls.registry:
            if account.pesel == pesel:
                return account
        return None

    @classmethod
    def delete_account_by_pesel(cls, pesel):
        account = cls.search_by_pesel(pesel)
        if account:
            cls.registry.remove(account)
            return True
        return False

    @classmethod
    def update_account(cls, pesel, imie=None, nazwisko=None):
        account = cls.search_by_pesel(pesel)
        if account:
            if imie is not None:
                account.imie = imie
            if nazwisko is not None:
                account.nazwisko = nazwisko
            return True
        return False

    @classmethod
    def clear_registry(cls):
        cls.registry = []

    @classmethod
    def is_pesel_unique(cls, pesel):
        return cls.search_by_pesel(pesel) is None

    @classmethod
    def dump_backup(cls, file_path: str):
        personal_accounts = [
            {"imie": acc.imie, "nazwisko": acc.nazwisko, "pesel": acc.pesel, "saldo": acc.saldo}
            for acc in cls.registry if isinstance(acc, KontoOsobiste)
        ]
        with open(file_path, 'w') as file:
            json.dump(personal_accounts, file)
        print(f"plik {file_path} został utworzony")

    @classmethod
    def load_backup(cls, file_path: str):
        with open(file_path, 'r') as file:
            data = json.load(file)
        cls.clear_registry()
        for acc in data:
            cls.add_account(KontoOsobiste(acc['imie'], acc['nazwisko'], acc['pesel']))