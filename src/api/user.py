from flask_restful import Resource, reqparse
from database import get_user_workouts
from werkzeug import exceptions
from api.response import Response


# Create a GET request parser for the workout API
get_parser = reqparse.RequestParser(bundle_errors=True)
get_parser.add_argument('username', type=str, required=True, help="The user whose workouts we will fetch.")


class User(Resource):
    @staticmethod
    def get():
        try:
            user_query = get_parser.parse_args()
        except exceptions.BadRequest as err:
            return Response.client_error(
                status=err.code,
                message="Error: Missing " + str(err.data['message']),
                data=None
            )

        try:
            data = get_user_workouts(**user_query)
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
