from datetime import datetime
from flask import Flask, render_template, url_for, request
from flask_socketio import SocketIO
import requests
import json
import pyowm
import googlemaps

app = Flask(__name__, static_url_path='/static')
socketio = SocketIO(app)
now = datetime.now()
date = now.strftime("%Y")+"-"+now.strftime("%m")+"-"+now.strftime("%d")
test_date = '2022-01-30'
params = {
  'access_key': 'ca97067f353996f37afa2117c9107b37'
}
flight_information  = {}

weather_key = "1762906f52427514c462d643654533b6"
owm = pyowm.OWM(weather_key)
mgr = owm.weather_manager()

google_key = "AIzaSyDtNE7L1vc3I8ZU8emZdAMFoZJeplm1ypY"
gmaps = googlemaps.Client(key = google_key)



def strip_time_string(time_string):
    time_string = (time_string.split("T")[1]).split("+")[0]
    time_string = datetime.strptime(time_string,"%H:%M:%S")
    return time_string


def calc_now_time():
    now_time = datetime.now()
    current_time = now_time.strftime("%H:%M:%S")
    current_time=datetime.strptime(current_time,"%H:%M:%S")
    return current_time

def find_city(iata):
    params = {
    "key":"c71fff2ce5",
    "secret": "b109d0741b40414"
    }
    r = requests.get("https://www.air-port-codes.com/api/v1/single?iata=" + iata,params=params)
    return r

@app.route('/', methods = ["GET","POST"])
def start():
    if request.method == "POST":
        params["flight_iata"] = request.form.get("flight-entry")
        print(params)
        api_result = requests.get('http://api.aviationstack.com/v1/flights', params)
        api_response = api_result.json()
        # print(api_response)
        global flight_information
        for flights in api_response["data"]:
            if flights["flight_date"] == test_date:
                flight_information = flights

        # print(flight_information)

        hidden = "" if flight_information is not None else "is-hidden"
        arrival = (strip_time_string(flight_information["arrival"]["estimated"])) - calc_now_time()
        print("arrival "+str(arrival))
        flight_information["departure"]["scheduled"] = datetime.strftime(strip_time_string(flight_information["departure"]["scheduled"]),"%H:%M:%S")
        flight_information["arrival"]["estimated"] = datetime.strftime((strip_time_string(flight_information["arrival"]["estimated"])),"%H:%M:%S")
        print(flight_information["arrival"]["estimated"] )
        print(flight_information)
        return render_template('index.html', flight_information=flight_information, hidden = hidden, placeholder = params["flight_iata"], arrival = arrival)
    else:
        flight_information = {'flight': {'iata': None}, 'arrival': {'airport': None, 'estimated': None, 'name': None},'departure':{'airport':None},'airline':{'name':None}}
        return render_template('index.html', hidden="is-hidden", flight_information=flight_information, placeholder="Enter Flight IATA")
    
@app.route('/dashboard', methods = ["GET"])
def dashboard():
    # print(flight_information)
    return render_template("dashboard.html", flight_information=flight_information)

@app.route('/join', methods=["GET", "POST"])
def join():
    displayName = request.form.get("name", False)
    if request.method == 'POST':
        print(displayName)
        return render_template("flightchat.html", user=displayName)
    else:
        return render_template('join.html')

@app.route('/flightchat')
def flightchat():
    return render_template('flightchat.html')

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)

@app.route('/guide', methods = ["GET"])
def guide():
    # prepare info for requests
    iata = flight_information["arrival"]["iata"]
    r = find_city(iata)
    city = (r.json())["airport"]["city"]
    lat = (r.json())["airport"]["latitude"]
    lng = (r.json())["airport"]["longitude"]
    location = lat + "," + lng

    # Weather Forecast guide
    # Weather
    observation = mgr.weather_at_place(city)
    w = observation.weather
    status = w.status
    dstatus = w.detailed_status         # 'clouds'
    wind = w.wind()                  # {'speed': 4.6, 'deg': 330}
    humidity = w.humidity                # 87
    temp = w.temperature('fahrenheit')  # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}
    visibility = w.visibility_distance
    # # icon = "http://openweathermap.org/img/wn/${data.weather[0].icon}@2x.png"
    # print(w.icon)
    # forecast = mgr.forecast_at_place(city, 'daily')
    # # print(forecast.when_clear())

    # Forecast
    api_url = "https://api.openweathermap.org/data/2.5/onecall?lat=" + lat + "&lon=" + lng + "&exclude=minutely,hourly&appid=" + weather_key
    api_result = requests.get(api_url)
    api_response = api_result.json()
    daily = api_response["daily"]
    # print(daily)
    temps = []
    days = []
    
    for i in range(len(daily)):
        temp = daily[i]["temp"]["day"]
        print(temp)
        temps += [temp]
        days += [i + 1]
    legend = "Forecast 7 days"
    print("HEREEEEE")
    print(temps)
    print(days)

    # Restaurant guide
    restaurants_result  = gmaps.places_nearby(location=location, radius = 10000, type="restaurant")
    restaurants = restaurants_result["results"]
    # res_photos = []
    # for restaurant in restaurants:
    #     photo_ref = restaurant["photos"][0]["photo_reference"]
    #     url = "https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photo_reference=" + photo_ref + "&key=" + google_key
    #     res_photos += url

    # Point of interest guide
    pois_result  = gmaps.places_nearby(location=location, radius = 10000, type="point_of_interest")
    pois = pois_result["results"]

    weather = {"city": city, "status": status, "dstatus": dstatus, "wind": wind, "humidity": humidity, "temp": temp, "visibility": visibility}
    # print(weather)
    return render_template("guide.html", weather=weather, restaurants=restaurants, pois=pois, values=temps, labels=days, legend=legend)

@app.route('/faq', methods = ["GET"])
def faq():
    return render_template("faq.html")

if __name__ == "__main__":
    socketio.run(app, debug=True)