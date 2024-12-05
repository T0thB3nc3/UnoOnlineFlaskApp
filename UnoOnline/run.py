from os import environ
from WebApp import app,socketio


if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST','localhost')
    try:
        PORT = int(environ.get('SERVER_PORT','8000'))
    except ValueError:
        PORT = 8000
    socketio.run(app,host=HOST,port=PORT,debug=True)