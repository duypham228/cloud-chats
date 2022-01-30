import requests
from datetime import datetime
import json
now = datetime.now()

date = now.strftime("%Y")+"-"+now.strftime("%m")+"-"+now.strftime("%d")
params = {
  'access_key': '6982c8f3d7c66ea30604f89bfbc58608',
  'flight_iata': 'AA4010',
}

api_result = requests.get('http://api.aviationstack.com/v1/flights', params)
api_response = api_result.json()

print(api_response["data"])
for flights in api_response["data"]:
    if flights["flight_date"] == date:
        flight_information = flights

