from flask import Flask, render_template, url_for
from flask_socketio import SocketIO

app = Flask(__name__, static_url_path='/static')


@app.route('/')
def hello():
    return render_template('home.html')






if __name__ == "__main__":
    app.run(debug=True)