from datetime import datetime
from pony.orm import *

# Generate a database variable which represents our MySQL database.
db = Database()


class UserWorkoutData(db.Entity):
    """Python representation of User Workout Data Table
    """
    user_id = Required(int)
    start_time = Required(datetime)
    end_time = Required(datetime)
    repetitions = Required(int, size=16)
    weight = Required(int, size=16)
    exercise = Required(int, size=16)
    variant = Required(int, size=8)
    skeleton_data = Optional(bytes)

    PrimaryKey(user_id, start_time)


@db_session
def add_workout(user_id: int, start_time: datetime, end_time: datetime, repetitions: int, weight: int,
                exercise: int, variant: int) -> None:
    """Command to add workout to SQL table

    Args:
        user_id: The user ID who did the workout.
        start_time: The workout's start time.
        end_time: The workout's end time.
        repetitions: The number of repetitions in the set.
        weight: The weight of the set in kilograms.
        exercise: The exercise ID associated with the activity.
        variant: The variant of the activity. Left hand, right hand, etc.

    Returns:
        Nothing.
    """
    UserWorkoutData(
        user_id=user_id,
        start_time=start_time,
        end_time=end_time,
        repetitions=repetitions,
        weight=weight,
        exercise=exercise,
        variant=variant
    )


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
