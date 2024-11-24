import json
import requests

from oitrainslate import ServiceDetails

class RealTimeTimesDataLoader:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def retrieveStationInformationJson(self, stationCode: str, to_stationcode:str = "") -> str:
        request_url = f'https://api.rtt.io/api/v1/json/search/{stationCode}'
        if to_stationcode:
            request_url += f'/to/{to_stationcode}'
        response = requests.get(request_url,
                                auth=(self.username, self.password),
                                timeout=10)
        if not response.ok:
            response.raise_for_status()
        return response.text
    

    def retrieveServicesFromSearch(self, departure_station_code: str, destination_station_code: str):
        station_info = self.retrieveStationInformationJson(departure_station_code, destination_station_code)
        parsed_info = json.loads(station_info)
        services = parsed_info['services']
        service_details = []
        for service in services:
            service_json = self.retrieveServiceJson(service['serviceUid'], service['runDate'])
            service_details.append(ServiceDetails.create_from_json(json.dumps(service_json)))
        return service_details
    

    def retrieveServiceJson(self, service_uid: str, run_date: str):
        formatted_run_date = run_date.replace("-", "/")
        service_url = f"https://api.rtt.io/api/v1/json/service/{service_uid}/{formatted_run_date}"
        response = requests.get(service_url,
                                auth=(self.username, self.password),
                                timeout=10)
        if not response.ok:
            response.raise_for_status()
        return response.json()