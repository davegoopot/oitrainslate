import requests
import os
from dotenv import load_dotenv

load_dotenv()

username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')

def test_realtraintimes_api_response():
    response = requests.get('https://api.rtt.io/api/v1/json/search/BWD', auth=(username, password))
    assert response.status_code == 200
    print(response.json())
