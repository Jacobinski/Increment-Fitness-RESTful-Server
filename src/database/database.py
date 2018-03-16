from datetime import datetime

from pony.orm import *

from constants import MIN_MONTH, MAX_MONTH, MIN_YEAR, REST_INTERVAL

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
def add_workout(user_id, start_time, end_time, repetitions, weight, exercise, variant, skeleton_data=None):
    """Command to add workout to SQL table

    :param user_id: (int) The user ID who did the workout.
    :param start_time: (int) The workout's start time in epoch.
    :param end_time: (int) The workout's end time in epoch.
    :param repetitions: (int) The number of repetitions in the set.
    :param weight: (int) The weight of the set in kilograms.
    :param exercise: (int) The exercise ID associated with the activity.
    :param variant: (int) The variant of the activity. Left hand, right hand, etc.
    :param skeleton_data: (bytes) A binary file for the skeleton activity file.
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
def get_workout(username, month, year):
    """Command to get a user's workout data from the SQL table.

    :param username: (str) The user whose data we will fetch.
    :param month: (int) The month of data to obtain in MM format.
    :param year: (int) The month of data to obtain in YYYY format.
    :return: An array of rows from the SQL table
    """

    def _format_output(_workouts):
        _workouts = [w.to_dict() for w in _workouts]
        _workouts.sort(key=lambda w: w['start_time'])
        output = []

        if len(_workouts) > 0:
            first_workout = _workouts[0]
            prev_exercise = first_workout['exercise']
            prev_exercise_start = first_workout['start_time']
            prev_set_end = first_workout['end_time']
            exercise = {
                'exerciseID': prev_exercise,
                'reps': [first_workout['repetitions']],
                'weights': [first_workout['weight']],
                'startTimes': [first_workout['start_time']],
                'endTimes': [first_workout['end_time']]
            }

            for ii in range(1, len(_workouts)):
                current_workout = _workouts[ii]
                current_set_start = current_workout['start_time']
                if current_workout['exercise'] == prev_exercise and current_set_start - prev_set_end < REST_INTERVAL:
                    exercise['reps'].append(current_workout['repetitions'])
                    exercise['weights'].append(current_workout['weight'])
                    exercise['startTimes'].append(current_set_start)
                    exercise['endTimes'].append(current_workout['end_time'])
                else:
                    output.append({
                        'date': prev_exercise_start,
                        'exercises': exercise
                    })
                    prev_exercise_start = current_workout['start_time']

                    exercise = {
                        'exerciseID': current_workout['exercise'],
                        'reps': [current_workout['repetitions']],
                        'weights': [current_workout['weight']],
                        'startTimes': [current_set_start],
                        'endTimes': [current_workout['end_time']]
                    }

                prev_exercise = current_workout['exercise']
                prev_set_end = current_workout['end_time']

            output.append({
                'date': prev_exercise_start,
                'exercises': exercise
            })

        return output

    if month < MIN_MONTH or month > MAX_MONTH or year < MIN_YEAR:
        raise ValueError('Invalid date passed into workout query')

    user_id = _get_user_id(username)
    if user_id is None:
        return None

    month_start_epoch = datetime(month=month, year=year, day=1).timestamp()
    if month == 12:
        month_end_epoch = datetime(month=1, year=year + 1, day=1).timestamp()
    else:
        month_end_epoch = datetime(month=month + 1, year=year, day=1).timestamp()

    workouts = select(workout for workout in UserWorkoutData
                      if (workout.user_id == user_id
                          and workout.start_time > month_start_epoch
                          and workout.start_time < month_end_epoch)
                      )[:]

    workouts = _format_output(workouts)

    # Ensure that query obtained results
    if len(workouts) > 0:
        result = {'username': username, 'data': workouts}
    else:
        result = None
    return result


@db_session
def _get_user_id(username):
    """ Command to convert a username to user id

    :param username: (str) The username of the account
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
