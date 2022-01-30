from amadeus import Client, ResponseError
amadeus = Client(client_id='RHfJtmQeGGjA6okKUcXL5SJ4MV21zpRs', client_secret='NpJ0Jf8O3JhVadoY')

try:
    '''
    Returns activities for a location based on geolocation coordinates
    '''
    response = amadeus.shopping.activities.get(latitude=40.414000, longitude=-3.691000, radius=20)
except ResponseError as error:
    raise error


response = str(response.data)

response = response.split('}')

print(*response, sep = "\n")