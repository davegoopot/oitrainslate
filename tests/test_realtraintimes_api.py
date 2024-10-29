import os

import requests
from dotenv import load_dotenv

load_dotenv()

username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')

def parse_response(response):
    departures = []
    for service in response['services']:
        scheduled_time = service['locationDetail']['gbttBookedDeparture']
        real_tme = service['locationDetail']['realtimeDeparture']
        departures.append((scheduled_time, real_tme))
    return departures

def test_realtraintimes_api_response():
    response = requests.get('https://api.rtt.io/api/v1/json/search/BWD',
                            auth=(username, password),
                            timeout=10)
    assert response.status_code == 200
    json_response = response.json()
    assert 'services' in json_response
    departures = parse_response(json_response)
    assert isinstance(departures, list)
    for departure in departures:
        assert isinstance(departure, tuple)
        assert len(departure) == 2
        assert isinstance(departure[0], str)
        assert isinstance(departure[1], str)
