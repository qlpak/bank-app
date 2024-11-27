import unittest
import requests

url = "http://127.0.0.1:5000/api/accounts"

class TestTransfersApi(unittest.TestCase):
    def setUp(self):
        self.pesel = "12345678901"
        self.target_pesel = "98765432109"

        requests.post(f"{url}", json={
            "imie": "marek",
            "nazwisko": "markowski",
            "pesel": self.pesel
        })
        requests.post(f"{url}", json={
            "imie": "anne",
            "nazwisko": "marie",
            "pesel": self.target_pesel
        })

        requests.post(f"{url}/{self.pesel}/transfer", json={
            "amount": 1000,
            "type": "incoming"
        })

    def tearDown(self):
        requests.delete(f"{url}/{self.pesel}")
        requests.delete(f"{url}/{self.target_pesel}")

    def test_incoming(self):
        response = requests.post(f"{url}/{self.pesel}/transfer", json={
            "amount": 500,
            "type": "incoming"
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "zlecenie przyjete")

        account_data = requests.get(f"{url}/{self.pesel}").json()
        self.assertEqual(account_data["saldo"], 1500)

    def test_outgoing_insufficient(self):
        response = requests.post(f"{url}/{self.pesel}/transfer", json={
            "amount": 2000,
            "type": "outgoing"
        })
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json()["message"], "target ne znaleziony lub za malo srodkow")

        account_data = requests.get(f"{url}/{self.pesel}").json()
        self.assertEqual(account_data["saldo"], 1000)

    def test_outgoing_success(self):
        response = requests.post(f"{url}/{self.pesel}/transfer", json={
            "amount": 500,
            "type": "outgoing",
            "target_pesel": self.target_pesel
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "zlecenie przyjete")

        sender_data = requests.get(f"{url}/{self.pesel}").json()
        self.assertEqual(sender_data["saldo"], 500)

        receiver_data = requests.get(f"{url}/{self.target_pesel}").json()
        self.assertEqual(receiver_data["saldo"], 500)

    def test_express(self):
        response = requests.post(f"{url}/{self.pesel}/transfer", json={
            "amount": 300,
            "type": "express",
            "target_pesel": self.target_pesel
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "zlecenie przyjete")

        sender_data = requests.get(f"{url}/{self.pesel}").json()
        self.assertEqual(sender_data["saldo"], 699)

        receiver_data = requests.get(f"{url}/{self.target_pesel}").json()
        self.assertEqual(receiver_data["saldo"], 300)

    def test_transfer_nonexistent(self):
        response = requests.post(f"{url}/00000000000/transfer", json={
            "amount": 500,
            "type": "incoming"
        })
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["message"], "nie znaleziono konta")

    def test_unknown_type(self):
        response = requests.post(f"{url}/{self.pesel}/transfer", json={
            "amount": 500,
            "type": "unknown"
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["message"], "nienznay typ przelewu")

    def test_missing_amount(self):
        response = requests.post(f"{url}/{self.pesel}/transfer", json={
            "type": "incoming"
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["message"], "kwota przelewu nieprawidlowa")

    def test_negative_amount(self):
        response = requests.post(f"{url}/{self.pesel}/transfer", json={
            "amount": -500,
            "type": "incoming"
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["message"], "kwota przelewu nieprawidlowa")

    def test_zero_amount(self):
        response = requests.post(f"{url}/{self.pesel}/transfer", json={
            "amount": 0,
            "type": "incoming"
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["message"], "kwota przelewu nieprawidlowa")
