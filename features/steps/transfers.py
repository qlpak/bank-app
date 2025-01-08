from behave import *
import requests
from unittest_assertions import AssertEqual

assert_equal = AssertEqual()
URL = "http://127.0.0.1:5000"

@given('I create an account using name: "{name}", last name: "{last_name}", pesel: "{pesel}", and saldo: "{saldo}"')
def create_account_with_saldo(context, name, last_name, pesel, saldo):
    json_body = {"name": name, "surname": last_name, "pesel": pesel, "saldo": int(saldo)}
    response = requests.post(URL + "/api/accounts", json=json_body)
    assert_equal(response.status_code, 201)

@when('I transfer {amount} zł from pesel: "{source_pesel}" to pesel: "{target_pesel}" as "{transfer_type}"')
def perform_transfer(context, amount, source_pesel, target_pesel, transfer_type):
    json_body = {
        "amount": int(amount),
        "type": transfer_type,
        "target_pesel": target_pesel
    }
    response = requests.post(URL + f"/api/accounts/{source_pesel}/transfer", json=json_body)
    assert_equal(response.status_code, 200)

@when('I transfer {amount} zł to pesel: "{pesel}" as "{transfer_type}"')
def perform_incoming_transfer(context, amount, pesel, transfer_type):
    json_body = {"amount": int(amount), "type": transfer_type}
    response = requests.post(URL + f"/api/accounts/{pesel}/transfer", json=json_body)
    assert_equal(response.status_code, 200)

@then('Account with pesel "{pesel}" has saldo equal to "{expected_saldo}"')
def check_account_saldo(context, pesel, expected_saldo):
    response = requests.get(URL + f"/api/accounts/{pesel}")
    assert_equal(response.status_code, 200)
    actual_saldo = response.json().get("saldo")
    assert_equal(str(actual_saldo), expected_saldo)
