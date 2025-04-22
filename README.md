# 💰 Bank Account System

A test-driven banking application built with Python and Flask. The system supports creating personal and company accounts, account registry management, transfers, loans, and transaction history emailing. It uses unit and behavioral testing (unittest + behave).

---

## 📦 Features

- ✅ Personal & Company account creation with validation
- 🔒 PESEL and NIP number verification
- 💸 Money transfers between accounts
- 🧾 Transaction history sent via email (SMTP)
- 💼 Loan functionality for personal and business use
- 🧪 Full test suite with `unittest` and `behave`

---

## 🚀 Getting Started

### Requirements

- Python 3.8+
- Install dependencies:

```bash
pip install -r requirments.txt
```

---

## 🏠 Project Structure

```
🔹 Account.py                  # Base account logic
🔹 CompanyAccount.py           # Business account class
🔹 PersonalAccount.py          # Personal account class
🔹 AccountRegistry.py          # Registry for all accounts
🔹 SMTPClient.py               # Email transaction history
🔹 api.py                      # Flask API with endpoints
🔹 tests/
│   🔹 test_create_personal_account.py
│   🔹 test_create_company_account.py
│   🔹 test_company_loan.py
│   🔹 test_personal_loan.py
│   🔹 test_send_history_to_email.py
│   🔹 test_transfers.py
│   🔹 test_validate_nip.py
│   🔹 test_registry.py
🔹 test_api/
│   🔹 test_api_transfers.py
│   🔹 test_api_crud.py
│   🔹 test_api_unique_pesel.py
│   🔹 test_api_backup.py
🔹 performance_tests/
│   🔹 test_performance.py
🔹 features/
│   🔹 transfers.feature           # BDD scenario for money transfers
│   🔹 account_registry.feature    # BDD scenario for account registry
│   🔹 steps/
│       🔹 transfers.py            # Step definitions for transfer-related scenarios
│       🔹 account_registry.py     # Step definitions for registry CRUD operations
🔹 requirments.txt
```

---

## 🧪 Running Tests

To run unit tests:

```bash
python -m unittest discover
```

To run behavior-driven tests:

```bash
behave
```

To check test coverage:

```bash
coverage run -m unittest discover
coverage report -m
```

## 📘 License

MIT License. See `LICENSE` for details.

---

## ✍️ Author

Developed by Lukasz Kulpaczynski – student project using TDD and Flask for Automatic Testing education.
