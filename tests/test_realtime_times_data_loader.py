import os
import pytest
from oitrainslate.realtime_times_data_loader import RealTimeTimesDataLoader
from dotenv import load_dotenv

load_dotenv()

username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')

def test_retrieve_station_information_json():
    data_loader = RealTimeTimesDataLoader(username, password)
    station_code = 'MAN'
    result = data_loader.retrieveStationInformationJson(station_code)
    assert isinstance(result, str)
    assert result != ''
