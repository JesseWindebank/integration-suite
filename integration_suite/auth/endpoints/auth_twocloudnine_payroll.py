import os
import json
import requests
from simple_salesforce import Salesforce


class CloudNinePayrollSalesforceConnection:
    def __init__(self, credentials):
        self.sf = Salesforce(**credentials)

    def get_salesforce_connection(self):
        return self.sf


def get_credentials(vault_name, item_name):

    # retrieve environment variables
    apikey = os.environ.get('ONEPASSWORD_API_KEY')
    url = os.environ.get('ONEPASSWORD_URL')
    apiVersion = os.environ.get('ONEPASSWORD_API_VERSION')

    # define json payload
    payload = json.dumps({
        "vaultName": vault_name,
        "itemName": item_name
    })

    # define headers
    headers = {
        'Api-Key': apikey,
        'Content-Type': 'application/json'
    }

    # make request
    try:
        response = requests.post(url, headers=headers, data=payload)

        # Check if the response contains a valid JSON object
        try:
            response_data = response.json()
        except json.JSONDecodeError:
            raise KeyError("Invalid or empty JSON response")

        data = response_data.get('data')

        if 'error' in data:
            raise KeyError(data['error'])

        return {
            'username': data.get('username'),
            'password': data.get('password'),
            'security_token': data.get('token'),
            'version': apiVersion
        }
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        raise e


def get_sf_connection(vault_name="Jitterbit Integration Customer Users", item_name='Rene Demo Integration User'):
    credentials = get_credentials(vault_name, item_name)

    print(f'credentials: {credentials}')

    cloud_nine_payroll_conn = CloudNinePayrollSalesforceConnection(credentials)
    return cloud_nine_payroll_conn.get_salesforce_connection()
