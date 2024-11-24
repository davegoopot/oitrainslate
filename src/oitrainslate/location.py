"""
    Data class representing a location as returned by the RTT API.
"""

from dataclasses import dataclass
import json

@dataclass
class Location:
    stationCode: str
    bookedDeparture: str
    estimatedDeparture: str

    @classmethod
    def create_from_parsed_json(cls, data: dict):
        stationCode = data['crs']
        bookedDeparture = data.get('gbttBookedDeparture', '')
        estimatedDeparture = data.get('realtimeDeparture', '')
        return Location(stationCode, bookedDeparture, estimatedDeparture)
