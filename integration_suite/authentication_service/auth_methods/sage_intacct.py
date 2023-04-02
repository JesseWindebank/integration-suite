import os
import json
import requests


def get_credentials(vaultName, itemName):

    # retrieve environment variables
    url = os.environ.get('ONEPASSWORD_URL')
    apikey = os.environ.get('ONEPASSWORD_API_KEY')

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
            'company_id': response_data['company_id'],
            'user_id': response_data['user_id'],
            'user_password': response_data['user_password'],
            'sender_id': response_data['sender_id'],
            'sender_password': response_data['sender_password']
        }
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    except KeyError as e:
        error_data = response.json()['data']
        print(f"An error occurred: {error_data['error']}")


credentials = get_credentials('Sage Intacct', 'Intacct (DFP) - Sandbox')

print(credentials)
