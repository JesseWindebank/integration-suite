import os
import unittest
from auth.endpoints.auth_twocloudnine_payroll import get_credentials


class TestGetCredentialsIntegration(unittest.TestCase):
    def test_get_credentials_positive(self):
        valid_vault_name = os.environ.get('ONEPASSWORD_VAULT_NAME')
        valid_item_name = os.environ.get('ONEPASSWORD_ITEM_NAME')

        try:
            credentials = get_credentials(valid_vault_name, valid_item_name)
            self.assertIsNotNone(credentials)
            self.assertIn('username', credentials)
            self.assertIn('password', credentials)
            self.assertIn('security_token', credentials)
            self.assertIn('version', credentials)
        except Exception as e:
            self.fail(f"Unexpected exception occurred: {e}")

    def test_get_credentials_negative(self):
        invalid_vault_name = os.environ.get('ONEPASSWORD_INVALID_VAULT_NAME')
        invalid_item_name = os.environ.get('ONEPASSWORD_INVALID_ITEM_NAME')

        with self.assertRaises(KeyError):
            get_credentials(invalid_vault_name, invalid_item_name)


if __name__ == '__main__':
    unittest.main()
