from pony.orm import *
from exercise import _get_user_id
from tables import UserWorkoutData


@db_session
def get_user_workouts(username):
    """Command to get a set of all workouts for a given user

    :param username: (str) The user whose workouts are retrieved.
    :return: An array of rows from the SQL table
    """

    user_id = _get_user_id(username)
    workouts = select(w.workout_id for w in UserWorkoutData if w.user_id == user_id)[:]

    # Format output
    output = {'Workouts': workouts}

    return output
