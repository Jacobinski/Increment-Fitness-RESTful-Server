#!flask/bin/python
from flask import Flask
from flaskrun import flaskrun
from flask_restful import Api
from api import Exercise, Workout, Leaderboards
from flask_cors import CORS

# Setup the application and RESTful API code
app = Flask(__name__)
api = Api(app)
CORS(app)

# Setup endpoints
api.add_resource(Exercise, '/api/exercises')
api.add_resource(Workout, '/api/workouts')
api.add_resource(Leaderboards, '/api/leaderboards')

# Run the application
if __name__ == '__main__':
    flaskrun(app)
