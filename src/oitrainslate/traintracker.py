import os
from typing import List
from oitrainslate import RealTimeTimesDataLoader, ServiceDetails
from dotenv import load_dotenv
import sys


def parse_args():
    if len(sys.argv) != 3:
        print("Usage: traintracker.py <from_station> <to_station>")
        sys.exit(1)
    return (sys.argv[1].upper(), sys.argv[2].upper())


def create_real_time_times_data_loader():
    load_dotenv()
    username = os.getenv('RTTUSERNAME')
    password = os.getenv('RTTPASSWORD')
    return RealTimeTimesDataLoader(username, password)


def print_results(results: List[ServiceDetails], from_station: str):
    departure_data = [
        [location for location in service.calling_points if location.stationCode == from_station]
        for service in results
        ]
    for loc in departure_data:
        print(f"Service {loc[0].stationCode} {loc[0].bookedDeparture} {loc[0].estimatedDeparture}")
    


def main():
    (from_station, to_station) = parse_args()
    rtt_data_loader = create_real_time_times_data_loader()
    results = rtt_data_loader.retrieveServicesFromSearch(from_station, to_station)
    print_results(results, from_station)
