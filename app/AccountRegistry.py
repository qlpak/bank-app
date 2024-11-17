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