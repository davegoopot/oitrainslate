"""
    Class representing the details of a single train service.
"""

from dataclasses import dataclass
from datetime import datetime
from .location import Location
import json


@dataclass
class ServiceDetails:
    service_id: str
    run_date: datetime.date
    calling_points: tuple[Location]
    
    @classmethod
    def create_from_json(cls, json_data):
        all_json = json.loads(json_data)
        service_id = all_json['serviceUid']
        run_date = all_json['runDate']
        run_date = datetime.strptime(all_json['runDate'], '%Y-%m-%d').date()
        calling_points = tuple(Location.create_from_parsed_json(loc) for loc in all_json['locations'])
        return ServiceDetails(service_id, run_date, calling_points)
    
    def stops_at(self, station):
        return station in self.calling_points
    

    def extractDepartureData(self, departure_statation:str)->Location:
        return next((loc for loc in self.calling_points if loc.stationCode == departure_statation), None)