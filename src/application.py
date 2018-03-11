#!flask/bin/python
from flask import Flask
from flaskrun import flaskrun
from flask_restful import Api
from api import Workout

# Setup the application and RESTful API code
app = Flask(__name__)
api = Api(app)

# Setup endpoints
api.add_resource(Workout, '/workouts')

# Run the application
if __name__ == '__main__':
    flaskrun(app)
