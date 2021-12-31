import requests
import os
from dotenv import load_dotenv

load_dotenv()

authURL = 'https://id.twitch.tv/oauth2/token'
Client_ID = os.getenv('CLIENT_ID')
Secret = os.getenv('SECRET')
API_KEY_YOUTUBE = os.getenv('YOUTUBE')

params = {
    'client_id': Client_ID,
    'client_secret': Secret,
    'grant_type': 'client_credentials'
}

def access_token():
    response = requests.post(url=authURL, params=params)
    return "Bearer " + response.json()['access_token']
