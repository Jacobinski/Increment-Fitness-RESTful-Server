from flask_restful import Resource, reqparse
from database import add_workout, get_workout, update_workout
from werkzeug import exceptions
from werkzeug.exceptions import HTTPException
from api.response import Response

# Create a POST request parser for the workout API
post_parser = reqparse.RequestParser(bundle_errors=True)
post_parser.add_argument('user_id', type=int, required=True, help="The user ID who did the workout.")
post_parser.add_argument('title', type=str, required=True, help="The name of the workout.")
post_parser.add_argument('date', type=int, required=True, help="Epoch time of the workout")

# Create a GET request parser for the workout API
get_parser = reqparse.RequestParser(bundle_errors=True)
get_parser.add_argument('workout_id', type=int, required=True, help="The ID of the workout.")

# Create a PATCH request parser for the workout API
patch_parser = reqparse.RequestParser(bundle_errors=True)
patch_parser.add_argument('workout_id', type=int, required=True, help="The ID of the workout.")
patch_parser.add_argument('title', type=str, required=True, help="The name of the workout.")
patch_parser.add_argument('date', type=int, required=True, help="Epoch time of the workout")


class Workout(Resource):
    @staticmethod
    def post():
        # Parse the input args
        try:
            workout_info = post_parser.parse_args()
        except HTTPException as err:
            return Response.client_error(
                status=err.code,
                message="Error: Missing " + str(err.data['message']),
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
        except Exception as err:
            return Response.client_error(
                status=400,
                message="Error: Database post error " + str(err.message),
                data=None
            )

    @staticmethod
    def get():
        # Parse the input args
        try:
            workout_query = get_parser.parse_args()
        except exceptions.BadRequest as err:
            return Response.client_error(
                status=err.code,
                message="Error: Missing " + str(err.data['message']),
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

    @staticmethod
    def patch():
        # Parse the input args
        try:
            workout_patch = get_parser.parse_args()
        except exceptions.BadRequest as err:
            return Response.client_error(
                status=err.code,
                message="Error: Missing " + str(err.data['message']),
                data=None
            )
        # Update workouts from database
        try:
            update_workout(**workout_patch)
            return Response.success(
                status=200,
                message="Successful GET of page",
                data=None
            )

        except Exception as err:
            return Response.server_error(
                status=400,                             # TODO: Create proper status for server error
                message="Server Error: {}".format(err)
            )
