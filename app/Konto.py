class Konto:
    def __init__(self, imie, nazwisko, pesel, kod_rabatowy=None):
        self.imie = imie
        self.nazwisko = nazwisko
        self.saldo = 0

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