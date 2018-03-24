from flask_restful import Resource, reqparse
from database import get_leaderboards
from werkzeug import exceptions
from api.response import Response


class Leaderboards(Resource):
    @staticmethod
    def get():
        # Fetch workouts from database
        try:

            data = get_leaderboards()
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
