from flask import Flask, request, jsonify
from app.AccountRegistry import AccountRegistry
from app.PersonalAccount import KontoOsobiste
app = Flask(__name__)
import os
@app.route("/api/accounts", methods=['POST'])
def create_account():
    data = request.get_json()
    saldo = data.get("saldo")
    konto = KontoOsobiste(data["name"], data["surname"], data["pesel"])
    konto.saldo = saldo
    AccountRegistry.add_account(konto)
    return jsonify({"message": "Account created"}), 201

@app.route("/api/accounts/<pesel>", methods=['GET'])
def get_account_by_pesel(pesel):
    account = AccountRegistry.search_by_pesel(pesel)
    if account is None:
        return jsonify({"message": "konta brak"}), 404
    return jsonify({
        "name": account.name,
        "surname": account.surname,
        "pesel": account.pesel,
        "saldo": account.saldo
    }), 200


@app.route("/api/accounts/<pesel>", methods=['PATCH'])
def update_account(pesel):
    data = request.get_json()
    account = AccountRegistry.search_by_pesel(pesel)

    if account is None:
        return jsonify({"message": "Account not found"}), 404

    AccountRegistry.update_account(
        pesel,
        name=data.get("name"),
        surname=data.get("surname")
    )
    return jsonify({"message": "Account updated"}), 200

@app.route("/api/accounts/<pesel>", methods=['DELETE'])
def delete_account(pesel):
    if AccountRegistry.delete_account_by_pesel(pesel):
        return jsonify({"message": "Account deleted"}), 200
    return jsonify({"message": "Account not found"}), 404

@app.route("/api/accounts/all", methods=['DELETE'])
def delete_all_accounts():
    AccountRegistry.clear_registry()
    return jsonify({"message": "All accounts deleted"}), 200

@app.route("/api/accounts/count", methods=['GET'])
def count_accounts():
    count = AccountRegistry.get_accounts_count()
    return jsonify({"count": count}), 200


@app.route("/api/accounts/unique", methods=['POST'])
def create_account_with_unique_pesel():
    data = request.get_json()

    if not AccountRegistry.is_pesel_unique(data["pesel"]):
        return jsonify({"message": "PESEL already exists"}), 409

    konto = KontoOsobiste(data["name"], data["surname"], data["pesel"])
    AccountRegistry.add_account(konto)
    return jsonify({"message": "Account created"}), 201

@app.route("/api/accounts/<pesel>/transfer", methods=['POST'])
def transfer_funds(pesel):
    data = request.get_json()
    account = AccountRegistry.search_by_pesel(pesel)
    if account is None:
        return jsonify({"message": "nie znaleziono konta"}), 404

    transfer_type = data.get("type")
    amount = data.get("amount", 0)

    if amount <= 0:
        return jsonify({"message": "kwota przelewu nieprawidlowa"}), 400

    if transfer_type == "incoming":
        account.przelew_przychodzacy(amount)
    elif transfer_type == "outgoing":
        target_account = AccountRegistry.search_by_pesel(data.get("target_pesel"))
        if not target_account:
            return jsonify({"message": "nie znaleziono konta"}), 422
        if not account.przelew_wychodzacy(amount, target_account):
            return jsonify({"message": "target ne znaleziony lub za malo srodkow"}), 422
    elif transfer_type == "express":
        target_account = AccountRegistry.search_by_pesel(data.get("target_pesel"))
        if not target_account:
            return jsonify({"message": "nie znaleziono konta"}), 422
        if not account.przelew_ekspresowy(amount, target_account):
            return jsonify({"message": "target ne znaleziony lub za malo srodkow"}), 422

    return jsonify({"message": "zlecenie przyjete"}), 200

@app.route("/api/accounts/backup/dump", methods=['POST'])
def dump_backup():
    file_path = "backup.json"
    AccountRegistry.dump_backup(file_path)
    return jsonify({"message": f"backup saved to {file_path}"}), 200

@app.route("/api/accounts/backup/load", methods=['POST'])
def load_backup():
    file_path = "backup.json"
    try:
        if not os.path.exists(file_path):
            return jsonify({"message": "backup file not found;("}), 404
        AccountRegistry.load_backup(file_path)
        return jsonify({"message": "Backup loaded successfully"}), 200
    except FileNotFoundError:
        return jsonify({"message": "backup file not found;("}), 404
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500
