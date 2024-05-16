import requests
import json

def test_server():
    url = "http://127.0.0.1:5004/weather"
    response = requests.post(url, data=json.dumps({"city":"北京"}))
    print(response.json())

if __name__ == "__main__":
    test_server()