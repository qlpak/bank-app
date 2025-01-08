from .Konto import Konto
from datetime import datetime

class KontoOsobiste(Konto):
    def __init__(self, name, surname, pesel, kod_rabatowy=None):
        super().__init__(name, surname, pesel, kod_rabatowy)

    def przelew_ekspresowy(self, kwota, konto_docelowe):
        oplata = 1
        if self.saldo >= kwota + oplata:
            self.saldo -= (kwota + oplata)
            konto_docelowe.przelew_przychodzacy(kwota)
            self.historia.append(-kwota)
            self.historia.append(-oplata)
            return True
        return False

    def czy_spelniony_warunek_I(self):
        return len(self.historia) >= 3 and all(transakcja > 0 for transakcja in self.historia[-3:])

    def czy_spelniony_warunek_II(self, kwota):
        return len(self.historia) >= 5 and sum(self.historia[-5:]) > kwota

    def zaciagnij_kredyt(self, kwota):
        if self.czy_spelniony_warunek_I() or self.czy_spelniony_warunek_II(kwota):
            self.saldo += kwota
            return True
        return False

    def send_history_to_email(self, email_address, smtp_client):
        subject = f"Wyciąg z dnia {datetime.today().strftime('%Y-%m-%d')}"
        text = f"twoja historia konta to: {self.historia}"
        return smtp_client.send(subject, text, email_address)