import requests

class RealTimeTimesDataLoader:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def retrieveStationInformationJson(self, stationCode: str) -> str:
        response = requests.get(f'https://api.rtt.io/api/v1/json/search/{stationCode}',
                                auth=(self.username, self.password),
                                timeout=10)
        return response.text
