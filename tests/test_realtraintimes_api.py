import os

import requests
from dotenv import load_dotenv
from oitrainslate.realtraintimes import parse_response, TrainJourney

load_dotenv()

username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')

def test_realtraintimes_api_response():
    response = requests.get('https://api.rtt.io/api/v1/json/search/BWD',
                            auth=(username, password),
                            timeout=10)
    assert response.status_code == 200
    json_response = response.json()
    assert 'services' in json_response
    journeys = parse_response(json_response)
    assert isinstance(journeys, list)
    for journey in journeys:
        assert isinstance(journey, TrainJourney)
        assert isinstance(journey.departure_station, str)
        assert isinstance(journey.departure_time, str)
        assert isinstance(journey.stations, list)
        for station in journey.stations:
            assert isinstance(station, str)
