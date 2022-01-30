import requests
from datetime import datetime
import json
now = datetime.now()

date = now.strftime("%Y")+"-"+now.strftime("%m")+"-"+now.strftime("%d")
params = {
  'access_key': 'd7c3fddb391eaebbf5f869ba00a784b8',
  'flight_iata': 'NK703',
}

api_result = requests.get('http://api.aviationstack.com/v1/flights', params)
api_response = api_result.json()

<<<<<<< HEAD
print(api_response["data"])
for flights in api_response["data"]:
    if flights["flight_date"] == date:
        flight_information = flights

=======
api_response = str(api_response)

api_response = api_response.split(',')

print(*api_response, sep = "\n")
>>>>>>> 1abd1130d4d8db158707352bea5a63bc1c52dc89
