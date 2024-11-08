"""
    These test are for experimentally testing the realtraintimes API. They are
    not part of the final implementation, but are useful for understanding how
    the API works and how to parse the data.
"""

import json
import os
import re

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


def extract_calling_points(service_data):
    calling_points = []
    for location in service_data['locations']:
        if location["isPublicCall"]:
            calling_points.append({
                "station_description": location['description'],
            })
    return calling_points



def test_loading_service_data():
    """
    First call the search API to get the serviceUid and runDate for a service
    Then call the service API to get the service data
    """

    search_response = requests.get('https://api.rtt.io/api/v1/json/search/BWD',
                            auth=(username, password),
                            timeout=10)
    assert search_response.status_code == 200
    journeys = parse_response(search_response.json())
    journey = journeys[0]
    serviceuid = journey["serviceuid"]
    rundate = journey["rundate"]
    formattedRunDate = rundate.replace("-", "/")

    serviceURL = f"https://api.rtt.io/api/v1/json/service/{serviceuid}/{formattedRunDate}"
    # The end of the URL should be <serviceUid>/<year>/<month>/<day>
    regexCheckUrlEnd = r".*[A-Z][0-9]{5}\/[0-9]{4}\/[0-9]{2}\/[0-9]{2}$"
    assert re.match(regexCheckUrlEnd, serviceURL), f"URL '{serviceURL}' does not match regex"

    serviceResponse = requests.get(serviceURL, auth=(username, password), timeout=10)
    assert serviceResponse.status_code == 200

    serviceData = serviceResponse.json()
    with open('service_data.json', 'w') as f:
        json.dump(serviceData, f, indent=4)

    callingPoints = extract_calling_points(serviceData)
    assert isinstance(callingPoints, list)
    assert len(callingPoints) > 0
    for callingPoint in callingPoints:
        assert isinstance(callingPoint["station_description"], str)
        assert callingPoint["station_description"] != ""
        print(callingPoint["station_description"])
    
