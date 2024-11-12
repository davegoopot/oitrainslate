
import json
import os
import pytest
from oitrainslate import RealTimeTimesDataLoader
from dotenv import load_dotenv

load_dotenv()

username = os.getenv('RTTUSERNAME')
password = os.getenv('RTTPASSWORD')

def test_retrieve_station_information_json():
    data_loader = RealTimeTimesDataLoader(username, password)
    station_code = 'MAN'
    result = data_loader.retrieveStationInformationJson(station_code)
    assert isinstance(result, str)
    assert result != ""


def test_retrieve_station_information_json_filtered_by_to():
    data_loader = RealTimeTimesDataLoader(username, password)
    departure_station_code = "MAN"
    destination_station_code = "EUS"
    result = data_loader.retrieveStationInformationJson(departure_station_code, destination_station_code)
    parsed_result = json.loads(result)
    destinations = [service["locationDetail"]["destination"][0]["tiploc"] for service in parsed_result["services"]]

    assert all(destination == "EUSTON" for destination in destinations)


