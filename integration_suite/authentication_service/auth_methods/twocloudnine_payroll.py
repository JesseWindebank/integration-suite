import os
import json
import requests
from simple_salesforce import Salesforce


class CloudNinePayrollSalesforceConnection:
    def __init__(self, credentials):
        self.sf = Salesforce(**credentials)

    def get_salesforce_connection(self):
        return self.sf


def get_credentials():

    # retrieve environment variables
    apikey = os.environ.get('ONEPASSWORD_API_KEY')
    url = os.environ.get('ONEPASSWORD_URL')
    vaultName = os.environ.get('ONEPASSWORD_VAULT_NAME')
    itemName = os.environ.get('ONEPASSWORD_ITEM_NAME')
    apiVersion = os.environ.get('ONEPASSWORD_API_VERSION')

    payload = json.dumps({
        "vaultName": vaultName,
        "itemName": itemName
    })
    headers = {
        'Api-Key': apikey,
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, data=payload)
    return {
        'username': response.json()['data']['username'],
        'password': response.json()['data']['password'],
        'security_token': response.json()['data']['token'],
        'version': apiVersion
    }


credentials = get_credentials()
cloud_nine_payroll_conn = CloudNinePayrollSalesforceConnection(credentials)
sf = cloud_nine_payroll_conn.get_salesforce_connection()
