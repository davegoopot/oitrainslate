""" 
    Tests that test the creation of ServiceDetails objects from the JSON data.
"""

import os
from oitrainslate import ServiceDetails
from datetime import datetime
import pytest


@pytest.fixture
def service_details_from_json():
    test_dir = os.path.dirname(__file__)
    with open(os.path.join(test_dir, 'service_example.json')) as f:
        service_json = f.read()
    return ServiceDetails.create_from_json(service_json)

def test_create_service_details_from_json(service_details_from_json):
    service_details = service_details_from_json
    assert service_details.service_id == "C42381"
    assert service_details.run_date == datetime(2024, 11, 8).date()
    expected_calling_points = [
        "LIV"
        , "LPY"
        , "WAW"
        , "WAC"
        , "BWD"
        , "IRL"
        , "MCO"
        , "MAN"
        , "SPT"
        , "SHF"
        , "MHS"
        , "DON"
        , "SCU"
        , "BTB"
        , "HAB"
        , "GMB"
        , "CLE"
    ]

    calling_points = [loc.stationCode for loc in service_details.calling_points]
    assert calling_points == expected_calling_points


def test_stops_at_one_station():
    service_details = ServiceDetails("dummy id", datetime(2024, 11, 8).date(), ("STATION1",))
    assert service_details.stops_at("STATION1")
    assert not service_details.stops_at("STATION2")

def test_stops_at_multiple_stations():
    service_details = ServiceDetails("dummy id", datetime(2024, 11, 8).date(), ("STATION1", "STATION2", "STATION3"))
    assert service_details.stops_at("STATION1")
    assert service_details.stops_at("STATION2")
    assert service_details.stops_at("STATION3")
    assert not service_details.stops_at("STATION4")

def test_stops_at_no_stations():
    service_details = ServiceDetails("dummy id", datetime(2024, 11, 8).date(), ())
    assert not service_details.stops_at("STATION1")


def test_service_departure_time(service_details_from_json):
    service_details = service_details_from_json
    departure_statation = "BWD"

    location_data = service_details.extractDepartureData(departure_statation)
    assert location_data.bookedDeparture == "0750"
    assert location_data.estimatedDeparture == "0751"

