"""
    These test are for experimentally testing the realtraintimes API. They are
    not part of the final implementation, but are useful for understanding how
    the API works and how to parse the data.
"""

import os

import requests
from dotenv import load_dotenv


load_dotenv()

username = os.getenv('RTTUSERNAME')
password = os.getenv('RTTPASSWORD')

def parse_response(response):
    journeys = []
    for service in response['services']:
        departure_station = service['locationDetail']['origin'][0]['tiploc']
        departure_time = service['locationDetail']['gbttBookedDeparture']
        destination = service['locationDetail']['destination'][0]['tiploc']
        serviceuid = service['serviceUid']
        rundate = service['runDate']
        journeys.append({
            "departure_station": departure_station,
            "departure_time": departure_time,
            "destination": destination,
            "serviceuid": serviceuid,
            "rundate": rundate,
        })
    return journeys


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
        assert isinstance(journey["departure_station"], str)
        assert isinstance(journey["departure_time"], str)
        assert isinstance(journey["destination"], str)
        assert isinstance(journey["serviceuid"], str)
        assert isinstance(journey["rundate"], str)
