import requests
from datetime import datetime
import json
now = datetime.now()

date = now.strftime("%Y")+"-"+now.strftime("%m")+"-"+now.strftime("%d")
params = {
  'access_key': '2f8d95898fdb8b75b644c46f43ea6d8b',
  'flight_iata': 'NK703',
}

api_result = requests.get('http://api.aviationstack.com/v1/flights', params)
api_response = api_result.json()

print(api_response["data"])
