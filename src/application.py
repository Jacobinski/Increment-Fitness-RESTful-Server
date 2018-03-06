#!flask/bin/python
from datetime import datetime
from flask import Flask
from flaskrun import flaskrun
from flask_restful import Resource, Api, reqparse
from database import add_workout

# Setup the application and RESTful API code
app = Flask(__name__)
api = Api(app)

# Create a request parser for the API
parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('user_id', type=int, required=True, help="The user ID who did the workout.")
parser.add_argument('start_time', type=int, required=True, help="Datetime of workout's start time.")
parser.add_argument('end_time', type=int, required=True, help="Datetime of workout's end time")
parser.add_argument('repetitions', type=int, required=True, help="The number of repetitions in the set.")
parser.add_argument('weight', type=int, required=True, help="The weight of the set in kilograms.")
parser.add_argument('exercise', type=int, required=True, help="The exercise ID associated with the activity.")
parser.add_argument('variant', type=int, required=True, help="The variant of the activity. Left hand, right hand, etc.")
parser.add_argument('skeleton_data', type=bytes, required=False, help="A binary file for the skeleton activity file..")


class Workout(Resource):
    @staticmethod
    def post():
        workout_info = parser.parse_args()
        try:
            add_workout(**workout_info)
            return {'status': 'successful POST'}
        except TypeError as err:
            # User passed in an arg that was not the correct type for our database
            return {'status': 'Failed POST. ' + str(err)}, 400

    @staticmethod
    def get():
        return {'status': 'successful GET'}


# Setup endpoints
api.add_resource(Workout, '/', '/workouts')

# Run the application
if __name__ == '__main__':
    flaskrun(app)
