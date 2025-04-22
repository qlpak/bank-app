import unittest
from parameterized import parameterized
from unittest.mock import patch, MagicMock
from ..PersonalAccount import PersonalAccount
from ..CompanyAccount import CompanyAccount
from ..SMTPClient import SMTPClient
from datetime import datetime

class TestSendHistoryToEmail(unittest.TestCase):
    @parameterized.expand([
        ("company_success", [5000, -1000, 500], True, "firma@example.com",
         f"Wyciąg z dnia {datetime.today().strftime('%Y-%m-%d')}", "historia konta firmy to: [5000, -1000, 500]"),
        ("company_failure", [-500, 100, 200], False, "error@example.com",
         f"Wyciąg z dnia {datetime.today().strftime('%Y-%m-%d')}", "historia konta firmy to: [-500, 100, 200]")
    ])
    def test_send_history_company_account(self, _, history, smtp_response, email_address, expected_subject, expected_text):
        with patch("app.CompanyAccount.CompanyAccount.waliduj_nip", return_value=True) as mock_validate_nip:
            smtp_client = MagicMock()
            smtp_client.send.return_value = smtp_response

            account = CompanyAccount("Firma X", "1234567890")
            account.historia = history

            result = account.send_history_to_email(email_address, smtp_client)

            smtp_client.send.assert_called_once_with(expected_subject, expected_text, email_address)
            self.assertEqual(result, smtp_response)
            mock_validate_nip.assert_called_once()
    @parameterized.expand([
        ("personal_success", PersonalAccount("Lukasz", "X", "12345678901"), [100, -1, 500], True, "test@example.com",
         f"Wyciąg z dnia {datetime.today().strftime('%Y-%m-%d')}", "twoja historia konta to: [100, -1, 500]"),
        ("personal_failure", PersonalAccount("Y", "YY", "12345678901"), [50, -25, 75], False, "msms@example.com",
         f"Wyciąg z dnia {datetime.today().strftime('%Y-%m-%d')}", "twoja historia konta to: [50, -25, 75]"),
        ("company_success", CompanyAccount("Firma X", "1234567890"), [5000, -1000, 500], True, "firma@example.com",
         f"Wyciąg z dnia {datetime.today().strftime('%Y-%m-%d')}", "historia konta firmy to: [5000, -1000, 500]"),
        ("company_failure", CompanyAccount("Firma Y", "1234567890"), [-500, 100, 200], False, "error@example.com",
         f"Wyciąg z dnia {datetime.today().strftime('%Y-%m-%d')}", "historia konta firmy to: [-500, 100, 200]")
    ])
    def test_send_history_to_email(self, _, account, history, smtp_response, email_address, expected_subject, expected_text):
        smtp_client = MagicMock()
        smtp_client.send.return_value = smtp_response
        account.historia = history

        result = account.send_history_to_email(email_address, smtp_client)

        smtp_client.send.assert_called_once_with(expected_subject, expected_text, email_address)
        self.assertEqual(result, smtp_response, f"the expected result was {smtp_response} but unfortunalely it is actually {result}")


