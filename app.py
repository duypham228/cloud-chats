from datetime import datetime
from flask import Flask, render_template, url_for, request
import requests
import json
import pyowm

app = Flask(__name__, static_url_path='/static')
now = datetime.now()
date = now.strftime("%Y")+"-"+now.strftime("%m")+"-"+now.strftime("%d")
test_date = '2022-01-30'
params = {
  'access_key': 'b65e03793d485c13e775c51562bd4bd5'
}
flight_information  = {}

weather_key = "1762906f52427514c462d643654533b6"
owm = pyowm.OWM(weather_key)


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
    r = requests.get("https://www.air-port-codes.com/api/v1/single?iata=IAH",params=params)
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

@app.route('/guide', methods = ["GET"])
def guide():
    # observation = owm.weather_at_place()
    params["flight_iata"]
    return render_template("guide.html", flight_information=flight_information)

if __name__ == "__main__":
    app.run(debug=True)