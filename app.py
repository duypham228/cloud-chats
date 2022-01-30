from datetime import datetime
from time import time
from click import progressbar
from flask import Flask, render_template, url_for, request
import requests
import json
import pyowm

app = Flask(__name__, static_url_path='/static')
now = datetime.now()
date = now.strftime("%Y")+"-"+now.strftime("%m")+"-"+now.strftime("%d")
test_date = '2022-01-30'
params = {
  'access_key': 'ca97067f353996f37afa2117c9107b37'
}
flight_information  = {}

weather_key = "1762906f52427514c462d643654533b6"
owm = pyowm.OWM(weather_key)


def strip_time_string(time_string):
    print(time_string)
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
        print(api_response)
        global flight_information
        for flights in api_response["data"]:
            if flights["flight_date"] == test_date:
                flight_information = flights
        global arrival
        hidden = "" if flight_information is not None else "is-hidden"
        arrival = (strip_time_string(flight_information["arrival"]["estimated"])) - calc_now_time()
        print("arrival "+str(arrival))
        print(flight_information["arrival"]["estimated"] )
        print("arrival "+str(arrival))
        time1 = strip_time_string(flight_information["departure"]["scheduled"])
        time2 = strip_time_string(flight_information["arrival"]["estimated"])
        t = time2.time()
        seconds = (t.hour * 60 + t.minute) * 60 + t.second
        global progressvalue
        progressvalue = round(((time2-calc_now_time()).total_seconds()/(time2-time1).total_seconds()))*100
        print(progressvalue)
        flight_information["departure"]["scheduled"] = datetime.strftime(time1,"%H:%M:%S")
        flight_information["arrival"]["estimated"] = datetime.strftime(time2,"%H:%M:%S")
        print(flight_information["arrival"]["estimated"] )
        print(flight_information)
        return render_template('index.html', flight_information=flight_information, hidden = hidden, placeholder = params["flight_iata"], arrival = arrival)
    else:
        flight_information = {'flight': {'iata': None}, 'arrival': {'airport': None, 'estimated': None, 'name': None},'departure':{'airport':None},'airline':{'name':None}}
        return render_template('index.html', hidden="is-hidden", flight_information=flight_information, placeholder="Enter Flight IATA")
    
@app.route('/dashboard', methods = ["GET"])
def dashboard():
    return render_template("dashboard.html", flight_information=flight_information, arrival = arrival, progressvalue=progressvalue)

@app.route('/guide', methods = ["GET"])
def guide():
    # observation = owm.weather_at_place()
    params["flight_iata"]
    return render_template("guide.html", flight_information=flight_information)

@app.route('/attendant',methods =["GET","POST"])
def attendant():
    assistance_items = ["order","help","medical"]
    return render_template



if __name__ == "__main__":
    app.run(debug=True)