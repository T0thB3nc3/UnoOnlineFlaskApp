from flask import Flask
from flask_socketio import SocketIO
app = Flask(__name__)
app.config["SECRET_KEY"] = "Fl4sk1s4w3s0m3"
socketio = SocketIO(app)
from WebApp import routes