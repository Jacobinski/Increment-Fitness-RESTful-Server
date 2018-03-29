#!flask/bin/python
from flask import Flask
from flaskrun import flaskrun
from flask_restful import Api
from api import Exercise, Workout, Leaderboards, User, Users
from flask_cors import CORS
from flask_socketio import SocketIO
import notification

# Setup the application and RESTful API code
app = Flask(__name__)
app.config['SECRET_KEY'] = 'DBS_SECRET_KEY'
api = Api(app)
CORS(app)
socketio = SocketIO(app)

# Initialize the notifications
notification.init(socketio)

# Setup endpoints
api.add_resource(Exercise, '/api/exercises')
api.add_resource(Workout, '/api/workouts')
api.add_resource(Leaderboards, '/api/leaderboards')
api.add_resource(User, '/api/user')
api.add_resource(Users, '/api/users')

# Run the application
if __name__ == '__main__':
    flaskrun(app=app, socketio=socketio)
