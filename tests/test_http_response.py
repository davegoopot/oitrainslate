import requests

def test_http_response():
    response = requests.get('https://example.com')
    assert response.status_code == 200
