from pony.orm import *
from typing import Iterable
from constants import MIN_MONTH, MAX_MONTH, MIN_YEAR
from datetime import datetime


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


class UserInformationData(db.Entity):
    """Python representation of User Information Data Table
    """
    username = PrimaryKey(str)
    user_id = Required(int, unique=True)


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


@db_session
def get_workout(username: str, month: int, year: int) -> Iterable[UserWorkoutData]:
    """Command to get a user's workout data from the SQL table.

    :param username: The user whose data we will fetch.
    :param month: The month of data to obtain in MM format.
    :param year: The month of data to obtain in YYYY format.
    :return: An array of rows from the SQL table
    """
    def _format_output(input):
        input_dict = [i.to_dict() for i in input]
        output = {}

        '''
            {
		date: {hour, minute, second, day (1-31), month (0-11), year},
		workout: [
				{exerciseID: (0-10), reps: [], weights: [] },
				{exerciseID: (0-10), reps: [], weights: [] }
			]
	},
	    '''
        for i in input_dict:
            workout = {}
            workout['exerciseID'] = i['exercise']
            workout['reps'] = i['repetitions']
            workout['weights'] = i['weight']

            print(workout)
        pass

    if month < MIN_MONTH or month > MAX_MONTH or year < MIN_YEAR:
        raise ValueError('Invalid date passed into workout query')

    user_id = _get_user_id(username)
    if user_id is None:
        return None

    month_start_epoch = datetime(month=month, year=year, day=1).timestamp()
    if month == 12:
        month_end_epoch = datetime(month=1, year=year+1, day=1).timestamp()
    else:
        month_end_epoch = datetime(month=month+1, year=year, day=1).timestamp()

    workouts = select(workout for workout in UserWorkoutData
                      if (workout.user_id == user_id
                          and workout.start_time > month_start_epoch
                          and workout.start_time < month_end_epoch)
                      )[:]

    _format_output(workouts)

    # Ensure that query obtained results
    if len(workouts) > 0:
        result = [w.to_dict() for w in workouts]
    else:
        result = None
    return result


@db_session
def _get_user_id(username: str) -> int:
    """ Command to convert a username to user id

    :param username: The username of the account
    :return: The integer user ID associated with the account
    """
    user_id = select(u.user_id for u in UserInformationData if u.username == username).first()

    return user_id


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
