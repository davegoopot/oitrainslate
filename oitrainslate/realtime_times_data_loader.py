import requests

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
