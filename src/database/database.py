from pony.orm import *

# Generate a database variable which represents our MySQL database.
db = Database()


class UserWorkoutData(db.Entity):
    """Python representation of User Workout Data Table
    """
    user_id = Required(int)
    start_time = Required(int, size=32)
    end_time = Required(int, size=32)
    repetitions = Required(int, size=16)
    weight = Required(int, size=16)
    exercise = Required(int, size=16)
    variant = Required(int, size=8)
    skeleton_data = Optional(bytes)

    PrimaryKey(user_id, start_time)


@db_session
def add_workout(user_id: int, start_time: int, end_time: int, repetitions: int, weight: int,
                exercise: int, variant: int, skeleton_data: bytes = None) -> None:
    """Command to add workout to SQL table

    :param user_id: The user ID who did the workout.
    :param start_time: The workout's start time in epoch.
    :param end_time: The workout's end time in epoch.
    :param repetitions: The number of repetitions in the set.
    :param weight: The weight of the set in kilograms.
    :param exercise: The exercise ID associated with the activity.
    :param variant: The variant of the activity. Left hand, right hand, etc.
    :param skeleton_data: A binary file for the skeleton activity file.
    :return: Nothing.
    """

    UserWorkoutData(
        user_id=user_id,
        start_time=start_time,
        end_time=end_time,
        repetitions=repetitions,
        weight=weight,
        exercise=exercise,
        variant=variant,
        skeleton_data=skeleton_data
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
