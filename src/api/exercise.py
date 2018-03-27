from flask_restful import Resource, reqparse
from database import add_exercise, get_exercise
from werkzeug import exceptions
from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import HTTPException
from api.response import Response

# Create a POST request parser for the exercise API
post_parser = reqparse.RequestParser(bundle_errors=True)
post_parser.add_argument('user_id', type=int, required=True, help="The user ID who did the exercise.")
post_parser.add_argument('start_time', type=int, required=True, help="Datetime of exercise's start time.")
post_parser.add_argument('end_time', type=int, required=True, help="Datetime of exercise's end time")
post_parser.add_argument('repetitions', type=int, required=True, help="The number of repetitions in the set.")
post_parser.add_argument('weight', type=int, required=True, help="The weight of the set in kilograms.")
post_parser.add_argument('exercise', type=str, required=True, help="The string name of the activity.")
post_parser.add_argument('variant', type=str, required=True, help="The variant of the activity. Left hand, right hand, etc.")
post_parser.add_argument('skeleton_data', type=FileStorage, required=True, location='files',
                         help="A binary file for the skeleton activity file.")

# Create a GET request parser for the exercise API
get_parser = reqparse.RequestParser(bundle_errors=True)
get_parser.add_argument('username', type=str, required=True, help="The username whose data should be returned.")
get_parser.add_argument('month', type=int, required=True, help="The month of data to obtain in MM format.")
get_parser.add_argument('year', type=int, required=True, help="The month of data to obtain in YYYY format.")


class Exercise(Resource):
    @staticmethod
    def post():
        try:
            exercise_info = post_parser.parse_args()
        except HTTPException as err:
            return Response.client_error(
                status=err.code,
                message="Error: Missing " + str(err.data['message']),
                data=None
            )

        try:
            add_exercise(**exercise_info)
            return Response.success(
                status=200,                             # TODO: Extract status from add_workout
                message="Successful POST to exercise table",
                data=None
            )
        except Exception as err:
            return Response.client_error(
                status=400,
                message="Error: Database post error " + str(err.message),
                data=None
            )

    @staticmethod
    def get():
        try:
            exercise_query = get_parser.parse_args()
        except exceptions.BadRequest as err:
            return Response.client_error(
                status=err.code,
                message="Error: Missing " + str(err.data['message']),
                data=None
            )

        try:
            data = get_exercise(**exercise_query)
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
