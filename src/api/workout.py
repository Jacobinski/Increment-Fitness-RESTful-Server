from flask_restful import Resource, reqparse
from database import add_workout, get_workout
from werkzeug import exceptions
from api.response import Response

# Create a POST request parser for the workout API
post_parser = reqparse.RequestParser(bundle_errors=True)
post_parser.add_argument('user_id', type=int, required=True, help="The user ID who did the workout.")
post_parser.add_argument('start_time', type=int, required=True, help="Datetime of workout's start time.")
post_parser.add_argument('end_time', type=int, required=True, help="Datetime of workout's end time")
post_parser.add_argument('repetitions', type=int, required=True, help="The number of repetitions in the set.")
post_parser.add_argument('weight', type=int, required=True, help="The weight of the set in kilograms.")
post_parser.add_argument('exercise', type=int, required=True, help="The exercise ID associated with the activity.")
post_parser.add_argument('variant', type=int, required=True, help="The variant of the activity. Left hand, right hand, etc.")
post_parser.add_argument('skeleton_data', type=bytes, required=False, help="A binary file for the skeleton activity file..")

# Create a GET request parser for the workout API
get_parser = reqparse.RequestParser(bundle_errors=True)
get_parser.add_argument('username', type=str, required=True, help="The username whose data should be returned.")
get_parser.add_argument('month', type=int, required=True, help="The month of data to obtain in MM format.")
get_parser.add_argument('year', type=int, required=True, help="The month of data to obtain in YYYY format.")


class Workout(Resource):
    @staticmethod
    def post():
        # Parse the input args
        try:
            workout_info = post_parser.parse_args()
        except exceptions.BadRequest as err:
            return Response.client_error(
                status=err.code,
                message=err.description,
                data=None
            )

        # Use the input args
        try:
            add_workout(**workout_info)
            return Response.success(
                status=200,                             # TODO: Extract status from add_workout
                message="Successful POST to workout table",
                data=None
            )
        except TypeError as err:
            # User passed in an arg that was not the correct type for our database
            return Response.server_error(
                status=400,                             # TODO: Create proper status for server error
                message="Server Error: {}".format(err),
            )

    @staticmethod
    def get():
        # Parse the input args
        try:
            workout_query = get_parser.parse_args()
        except exceptions.BadRequest as err:
            return Response.client_error(
                status=err.code,
                message=err.description,
                data=None
            )

        # Fetch workouts from database
        try:

            data = get_workout(**workout_query)
            return Response.success(
                status=200,
                message="Successful GET of page",
                data=data
            )

        except Exception as err:
            return Response.server_error(
                status=400,                             # TODO: Create proper status for server error
                message="Server Error: {}".format(err)
            )
