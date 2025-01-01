import os
import requests
from datetime import datetime
from .Konto import Konto

class KontoFirmowe(Konto):
    def __init__(self, nazwa_firmy, nip):
        self.nazwa_firmy = nazwa_firmy
        self.nip = nip if len(nip) == 10 else "Niepoprawny NIP!"
        self.saldo = 0
        self.historia = []

        if len(nip) == 10:
            if not self.waliduj_nip(nip):
                raise ValueError("Company not registered!!")

    def waliduj_nip(self, nip):
        url = os.getenv("BANK_APP_MF_URL", "https://wl-test.mf.gov.pl") + f"/api/search/nip/{nip}?date={datetime.today().strftime('%Y-%m-%d')}"
        try:
            response = requests.get(url)
            return response.status_code == 200
        except Exception as e:
            raise ValueError("API error occurred while validating NIP")


    def przelew_ekspresowy(self, kwota, konto_docelowe):
        oplata = 5
        if self.saldo >= kwota + oplata:
            self.saldo -= (kwota + oplata)
            konto_docelowe.przelew_przychodzacy(kwota)
            self.historia.append(-kwota)
            self.historia.append(-oplata)
            return True
        return False

    def saldo_enough(self, kwota):
        return self.saldo >= 2 * kwota

    def zus_zaplacony(self):
        return any(transakcja == -1775 for transakcja in self.historia)

    def zaciagnij_kredyt(self, kwota):
        if self.saldo_enough(kwota) and self.zus_zaplacony():
            self.saldo += kwota
            return True
        return False

    def send_history_to_email(self, email_address, smtp_client):
        subject = f"Wyciąg z dnia {datetime.today().strftime('%Y-%m-%d')}"
        text = f"historia konta firmy to: {self.historia}"
        return smtp_client.send(subject, text, email_address)
