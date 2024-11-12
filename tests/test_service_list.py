""" 
    Tests that test the creation of ServiceDetails objects from the JSON data.
"""

import os
from oitrainslate import ServiceDetails
from datetime import datetime

def test_create_service_details_from_json():
    test_dir = os.path.dirname(__file__)
    with open(os.path.join(test_dir, 'service_example.json')) as f:
        service_json = f.read()

    service_details = ServiceDetails.create_from_json(service_json)
    assert service_details.service_id == "C42381"
    assert service_details.run_date == datetime(2024, 11, 8).date()
    expected_calling_points = (
        "LVRPLSH"
        , "ALERTN"
        , "WRGTWST"
        , "WRGT"
        , "BIRCHWD"
        , "IRLAM"
        , "MNCROXR"
        , "MNCRPIC"
        , "STKP"
        , "SHEFFLD"
        , "MEADWHL"
        , "DONC"
        , "SCNTHRP"
        , "BNTBY"
        , "HABRO"
        , "GRMSBYT"
        , "CLTHRPS"
    )

    assert service_details.calling_points == expected_calling_points
    assert type(service_details.calling_points) == tuple


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
    