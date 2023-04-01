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

    apikey = os.environ.get('ONEPASSWORD_API_KEY')

    url = "https://2CloudNine49807.jitterbit.cc/Production/1.0/retrieveCredentials"
    payload = json.dumps({
        "vaultName": "Jitterbit Integration Customer Users",
        "itemName": "Jitterbit User"
    })
    headers = {
        'Api-Key': apikey,
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, data=payload)
    return {
        'username': response.json()['username'],
        'password': response.json()['password'],
        'security_token': response.json()['token'],
        'version': '54.0'
    }


credentials = get_credentials()
cloud_nine_payroll_conn = CloudNinePayrollSalesforceConnection(credentials)
sf = cloud_nine_payroll_conn.get_salesforce_connection()
