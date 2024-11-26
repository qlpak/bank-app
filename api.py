from flask import Flask, request, jsonify
from app.AccountRegistry import AccountRegistry
from app.PersonalAccount import KontoOsobiste
app = Flask(__name__)
@app.route("/api/accounts", methods=['POST'])
def create_account():
    data = request.get_json()
    print(f"Create account request: {data}")
    konto = KontoOsobiste(data["imie"], data["nazwisko"], data["pesel"])
    AccountRegistry.add_account(konto)
    return jsonify({"message": "Account created"}), 201

@app.route("/api/accounts/<pesel>", methods=['GET'])
def get_account_by_pesel(pesel):
    account = AccountRegistry.search_by_pesel(pesel)
    if account is None:
        return jsonify({"message": "konta brak"}), 404
    return jsonify({
        "imie": account.imie,
        "nazwisko": account.nazwisko,
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
        imie=data.get("imie"),
        nazwisko=data.get("nazwisko")
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

