import json
import requests
import os


def get_config():
    # Read values from config.json file
    current_dir = os.path.dirname(__file__)

    with open(f'{current_dir}/config.json') as file:
        config = json.load(file)

    # Access specific values from the config.json file
    client_id = config['client_id']
    client_secret = config['client_secret']

    # Return the values
    return client_id, client_secret


def get_token():
    client_id, client_secret = get_config()

    # request token from the API
    token_url = 'https://login.microsoftonline.com/autodesk.onmicrosoft.com/oauth2/v2.0/token'
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'client_credentials',
        'scope': 'https://cognitiveservices.azure.com/.default'
    }
    response = requests.post(token_url, data=data)

    # check if the request was successful
    if response.status_code == 200:
        token = response.json()['access_token']
        return token
    else:
        raise Exception('Failed to get token from the API')
