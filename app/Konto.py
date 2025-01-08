class Konto:
    def __init__(self, name, surname, pesel, kod_rabatowy=None):
        self.name = name
        self.surname = surname
        self.saldo = 0
        self.historia = []

        if len(pesel) == 11:
            self.pesel = pesel
        else:
            self.pesel = "niepoprawny pesel"

        if self.czy_kod_poprawny(kod_rabatowy) and self.jaki_wiek(pesel):
            self.saldo += 50

    def czy_kod_poprawny(self, kod_rabatowy):
        if kod_rabatowy is None:
            return False
        if kod_rabatowy.startswith("PROM_") and len(kod_rabatowy) == 8:
            return True
        return False

    def jaki_wiek(self, pesel):
        yob = int(pesel[0:2])
        mob = int(pesel[2:4])

        if mob > 12:
            yob += 2000
        else:
            yob += 1900

        return yob > 1960

    def przelew_wychodzacy(self, kwota, konto_docelowe):
        if self.saldo >= kwota:
            self.saldo -= kwota
            konto_docelowe.przelew_przychodzacy(kwota)
            self.historia.append(-kwota)
            return True
        return False

    def przelew_przychodzacy(self, kwota):
        self.saldo += kwota
        self.historia.append(kwota)
