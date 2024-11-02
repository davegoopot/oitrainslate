from dataclasses import dataclass
from typing import List

@dataclass
class TrainJourney:
    departure_station: str
    departure_time: str
    stations: List[str]

def parse_response(response) -> List[TrainJourney]:
    journeys = []
    for service in response['services']:
        departure_station = service['locationDetail']['origin'][0]['tiploc']
        departure_time = service['locationDetail']['gbttBookedDeparture']
        stations = [stop['tiploc'] for stop in service['locationDetail']['locations']]
        journeys.append(TrainJourney(departure_station, departure_time, stations))
    return journeys
