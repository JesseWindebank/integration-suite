import json
import unittest
from unittest.mock import patch, MagicMock
import requests
from simple_salesforce import Salesforce
from authentication_service.auth_methods.twocloudnine_payroll import CloudNinePayrollSalesforceConnection, get_credentials


import sys
import os

sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', '..', '..')))


class TestCloudNinePayrollSalesforceConnection(unittest.TestCase):

    def test_init(self):
        test_credentials = {
            'username': 'test_username',
            'password': 'test_password',
            'security_token': 'test_security_token',
            'version': 'test_version'
        }

        with patch.object(Salesforce, '__init__', return_value=None) as mocked_salesforce:
            conn = CloudNinePayrollSalesforceConnection(test_credentials)
            mocked_salesforce.assert_called_once_with(**test_credentials)

    def test_get_salesforce_connection(self):

        username = os.environ.get('SFDC_JITTERBIT_USERNAME')
        password = os.environ.get('SFDC_JITTERBIT_PASSWORD')
        security_token = os.environ.get('SFDC_JITTERBIT_TOKEN')

        test_sf = MagicMock(spec=Salesforce)
        conn = CloudNinePayrollSalesforceConnection(
            {'username': username, 'password': password, 'security_token': security_token, 'version': '54.0'})
        conn.sf = test_sf
        self.assertEqual(conn.get_salesforce_connection(), test_sf)


class TestGetCredentials(unittest.TestCase):

    def test_get_credentials(self):
        test_data = {
            'username': 'test_username',
            'password': 'test_password',
            'token': 'test_security_token'
        }
        test_response = MagicMock()
        test_response.json.return_value = {'data': test_data}
        test_environ = {
            'ONEPASSWORD_API_KEY': 'test_api_key',
            'ONEPASSWORD_URL': 'test_url',
            'ONEPASSWORD_VAULT_NAME': 'test_vault_name',
            'ONEPASSWORD_ITEM_NAME': 'test_item_name',
            'ONEPASSWORD_API_VERSION': 'test_api_version'
        }

        with patch.dict(os.environ, test_environ):
            with patch.object(requests, 'post', return_value=test_response) as mocked_post:
                credentials = get_credentials()

                # Check if requests.post was called with the correct parameters
                expected_payload = json.dumps({
                    "vaultName": test_environ['ONEPASSWORD_VAULT_NAME'],
                    "itemName": test_environ['ONEPASSWORD_ITEM_NAME']
                })
                expected_headers = {
                    'Api-Key': test_environ['ONEPASSWORD_API_KEY'],
                    'Content-Type': 'application/json'
                }
                mocked_post.assert_called_once_with(
                    test_environ['ONEPASSWORD_URL'], headers=expected_headers, data=expected_payload)

                # Check if the returned credentials are as expected
                self.assertEqual(credentials, {
                    'username': test_data['username'],
                    'password': test_data['password'],
                    'security_token': test_data['token'],
                    'version': test_environ['ONEPASSWORD_API_VERSION']
                })


if __name__ == '__main__':
    unittest.main()
