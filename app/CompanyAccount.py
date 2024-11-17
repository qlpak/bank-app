from .Konto import Konto

class KontoFirmowe(Konto):
    def __init__(self, nazwa_firmy, nip):
        self.nazwa_firmy = nazwa_firmy
        self.nip = nip if len(nip) == 10 else "Niepoprawny NIP!"
        self.saldo = 0
        self.historia = []

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
