import json
import os
import pytest
from oitrainslate import RealTimeTimesDataLoader, ServiceDetails
from dotenv import load_dotenv

load_dotenv()

username = os.getenv('RTTUSERNAME')
password = os.getenv('RTTPASSWORD')

@pytest.fixture
def data_loader():
    return RealTimeTimesDataLoader(username, password)

def test_retrieve_station_information_json(data_loader):
    station_code = 'MAN'
    result = data_loader.retrieveStationInformationJson(station_code)
    assert isinstance(result, str)
    assert result != ""

def test_retrieve_station_information_json_filtered_by_to(data_loader):
    departure_station_code = "MAN"
    destination_station_code = "EUS"
    result = data_loader.retrieveStationInformationJson(departure_station_code, destination_station_code)
    parsed_result = json.loads(result)
    destinations = [service["locationDetail"]["destination"][0]["tiploc"] for service in parsed_result["services"]]

    assert all(destination == "EUSTON" for destination in destinations)

def test_retrieve_services_from_search(data_loader):
    departure_station_code = "BWD"
    destination_station_code = "URM"
    results = data_loader.retrieveServicesFromSearch(departure_station_code, destination_station_code)
    assert isinstance(results, list)
    assert len(results) > 0
    assert all(isinstance(result, ServiceDetails) for result in results)


