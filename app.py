from flask import Flask, render_template, url_for, request, redirect
from flask_socketio import SocketIO
import googlemaps
import requests

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'testingtesting'
socketio = SocketIO(app)

#GLOBAL ENV
API_KEY = "AIzaSyDtNE7L1vc3I8ZU8emZdAMFoZJeplm1ypY"
flight = "ABCD1234"
gmaps = googlemaps.Client(key = API_KEY)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/join_public', methods=["GET", "POST"])
def join_public():
    displayName = request.form.get("name", False)
    if request.method == 'POST':
        print(displayName)
        return render_template("session.html", user=displayName, room="Public")
    else:
        return render_template('join_public.html')

@app.route('/ask_attendant', methods=["GET", "POST"])
def ask_attendant():
    displayName = request.form.get("name", False)
    if request.method == 'POST':
        print(displayName)
        return render_template("privatesession.html", user=displayName, room="Attendant")
    else:
        return render_template('ask_attendant.html')

@app.route('/session')
def session():
    return render_template('session.html')

@app.route('/privatesession')
def privatesession():
    return render_template('privatesession.html')

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)


@app.route('/dashboard')
def dashboard():

    # url = "https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photo_reference=Aap_uEA7vb0DDYVJWEaX3O-AtYp77AaswQKSGtDaimt3gt7QCNpdjp1BkdM6acJ96xTec3tsV_ZJNL_JP-lqsVxydG3nh739RE_hepOOL05tfJh2_ranjMadb3VoBYFvF0ma6S24qZ6QJUuV6sSRrhCskSBP5C1myCzsebztMfGvm7ij3gZT&key=" + API_KEY
    
    restaurants_result  = gmaps.places_nearby(location='-33.8670522,151.1957362', radius = 10000, type="restaurant")
    restaurants = restaurants_result["results"]
    
    # point of interest
    pois_result  = gmaps.places_nearby(location='-33.8670522,151.1957362', radius = 10000, type="point_of_interest")
    pois = pois_result["results"]
    
    # print(places)
    
    return render_template("dashboard.html", restaurants=restaurants, pois=pois)






if __name__ == "__main__":
    socketio.run(app, debug=True)