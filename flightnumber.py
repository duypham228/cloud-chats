import requests

params = {
  'access_key': 'd7c3fddb391eaebbf5f869ba00a784b8',
  'flight_iata': 'PR2557'
}

api_result = requests.get('http://api.aviationstack.com/v1/flights', params)

api_response = api_result.json()

print(api_response)