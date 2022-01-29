from flask import Flask, render_template, url_for, request, redirect
from flask_socketio import SocketIO

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'testingtesting'
socketio = SocketIO(app)

#GLOBAL ENV
flight = "ABCD1234"

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/join', methods=["GET", "POST"])
def join():
    displayName = request.form.get("name", False)
    if request.method == 'POST':
        print(displayName)
        return render_template("session.html", user=displayName)
    else:
        return render_template('join.html')

@app.route('/session')
def session():
    return render_template('session.html')

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)



if __name__ == "__main__":
    socketio.run(app, debug=True)