import requests
params = {
    "key":"c71fff2ce5",
    "secret": "b109d0741b40414"
}
r = requests.get("https://www.air-port-codes.com/api/v1/single?iata=IAH",params=params)

print(r.text)
city = r.json()["airport"]["name"]
print(city)
r = requests.get("http://api.weatherapi.com/v1/current.json?key=4f7cf269ebbd468f82c14401223001&q="+city+"&aqi=no")
print(r.json()["current"]["temp_f"])


r=requests.get("https://api.yelp.com/v3/businesses/search")