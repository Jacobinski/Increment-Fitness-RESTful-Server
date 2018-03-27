from pony.orm import *

from exercise import _get_user_id
from workout import UserWorkoutData

# Generate a database variable which represents our MySQL database.
db = Database()


@db_session
def get_user_workouts(username):
    """Command to get a set of all workouts for a given user

    :param username: (str) The user whose workouts are retrieved.
    :return: An array of rows from the SQL table
    """

    user_id = _get_user_id(username)
    workouts = select(w.workout_id for w in UserWorkoutData if w.user_id == user_id)[:]

    return workouts


# Bind the database to the AWS RDS instance and create a mapping from classes to tables
# TODO: Remove the hardcoded values. This isn't good software practice, but fixing it requires setting up AWS Parameter
#       Store on each developer's machine and the cloud, which is going to be a ton of work.
db.bind(
    provider='mysql',
    host='increment.cx9kpie1sol8.us-west-1.rds.amazonaws.com',
    user='admin',
    passwd='L69VLKJTEwgJVBHNBt',
    db='increment_db')
db.generate_mapping(create_tables=True)
