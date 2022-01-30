from datetime import datetime
from flask import Flask, render_template, url_for, request
import requests
import json

app = Flask(__name__, static_url_path='/static')
now = datetime.now()
date = now.strftime("%Y")+"-"+now.strftime("%m")+"-"+now.strftime("%d")
params = {
  'access_key': '2d81d1352add1055528f544eb552ac04',
}

@app.route('/', methods = ["GET","POST"])
def start():
    if request.method == "POST":
        params["flight_iata"] = request.form.get("flight-entry")
        print(params)
        api_result = requests.get('http://api.aviationstack.com/v1/flights', params)
        api_response = api_result.json()
        flight_information = None
        for flights in api_response["data"]:
            if flights["flight_date"] == date:
                flight_information = flights
        hidden = "" if flight_information is not None else "is-hidden"
        print(flight_information)
        return render_template('index.html', flight_information=flight_information, hidden = hidden)
    else:
        flight_information = {'flight': {'iata': None}, 'arrival': {'airport': None, 'estimated': None, 'name': None}, 'airline':{'name':None}}
        return render_template('index.html', hidden="is-hidden", flight_information=flight_information)
    

if __name__ == "__main__":
    app.run(debug=True)