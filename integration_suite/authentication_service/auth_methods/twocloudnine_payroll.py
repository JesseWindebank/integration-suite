import os
import json
import requests
from simple_salesforce import Salesforce


class CloudNinePayrollSalesforceConnection:
    def __init__(self, credentials):
        self.sf = Salesforce(**credentials)

    def get_salesforce_connection(self):
        return self.sf


def get_credentials(vaultName, itemName):

    # retrieve environment variables
    apikey = os.environ.get('ONEPASSWORD_API_KEY')
    url = os.environ.get('ONEPASSWORD_URL')
    apiVersion = os.environ.get('ONEPASSWORD_API_VERSION')

    # define json payload
    payload = json.dumps({
        "vaultName": vaultName,
        "itemName": itemName
    })

    # define headers
    headers = {
        'Api-Key': apikey,
        'Content-Type': 'application/json'
    }

    # make request
    try:
        response = requests.post(url, headers=headers, data=payload)
        response_data = response.json()['data']
        return {
            'username': response_data.get('username'),
            'password': response_data.get('password'),
            'security_token': response_data.get('token'),
            'version': apiVersion
        }
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    except KeyError as e:
        error_data = response.json()['data']
        print(f"An error occurred: {error_data['error']}")


credentials = get_credentials(
    'Jitterbit Integration Customer Users', 'Jitterbit User')
cloud_nine_payroll_conn = CloudNinePayrollSalesforceConnection(credentials)
sf = cloud_nine_payroll_conn.get_salesforce_connection()
