from datetime import datetime
from pony.orm import *
from constants import MIN_MONTH, MAX_MONTH, MIN_YEAR, REST_INTERVAL
from base64 import encodestring
from tables import UserExerciseData, UserInformationData


@db_session
def add_exercise(user_id, start_time, end_time, repetitions, weight, exercise, variant, skeleton_data=''):
    """Command to add exercise to SQL table

    :param user_id: (int) The user ID who did the workout.
    :param start_time: (int) The workout's start time in epoch.
    :param end_time: (int) The workout's end time in epoch.
    :param repetitions: (int) The number of repetitions in the set.
    :param weight: (int) The weight of the set in kilograms.
    :param exercise: (str) The string name of the activity.
    :param variant: (str) The variant of the activity. Left hand, right hand, etc.
    :param skeleton_data: (bytes) An optional binary file for the skeleton activity file.
    :return: Nothing.
    """
    workout_id = _get_workout_id(_get_username(user_id))

    if workout_id is None:
        raise ValueError('This user does not appear to exist. Failed to add exercise')
    else:
        # Read the skeleton data file if it was added to the query
        if skeleton_data:
            skeleton_data = skeleton_data.read()

        UserExerciseData(
            user_id=user_id,
            workout_id=workout_id,
            start_time=start_time,
            end_time=end_time,
            repetitions=repetitions,
            weight=weight,
            exercise=exercise,
            variant=variant,
            skeleton_data=skeleton_data
        )


@db_session
def get_exercise(username, month, year):
    """Command to get a user's exercise data from the SQL table.

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
            if first_workout['skeleton_data']:
                picture = encodestring(first_workout['skeleton_data'])
            else:
                picture = None

            exercise = {
                'exercise': prev_exercise,
                'reps': [first_workout['repetitions']],
                'weights': [first_workout['weight']],
                'startTimes': [first_workout['start_time']],
                'endTimes': [first_workout['end_time']],
                'picture': picture
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
                    if current_workout['skeleton_data']:
                        picture = encodestring(current_workout['skeleton_data'])
                    else:
                        picture = None

                    exercise = {
                        'exercise': current_workout['exercise'],
                        'reps': [current_workout['repetitions']],
                        'weights': [current_workout['weight']],
                        'startTimes': [current_set_start],
                        'endTimes': [current_workout['end_time']],
                        'picture': picture
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

    epoch = datetime(month=1, year=1970, day=1)
    month_start_epoch = int((datetime(month=month, year=year, day=1) - epoch).total_seconds())
    if month == 12:
        month_end_epoch = int((datetime(month=1, year=year + 1, day=1) - epoch).total_seconds())
    else:
        month_end_epoch = int((datetime(month=month + 1, year=year, day=1) - epoch).total_seconds())

    exercises = select(exercise for exercise in UserExerciseData
                       if (exercise.user_id == user_id
                          and exercise.start_time > month_start_epoch
                          and exercise.start_time < month_end_epoch)
                      )[:]

    exercises = _format_output(exercises)

    # Ensure that query obtained results
    if len(exercises) > 0:
        result = {'username': username, 'data': exercises}
    else:
        result = None
    return result


@db_session
def get_leaderboards():
    """Command to get total reps done by each user.

    :return: An array of rows from the SQL table
    """
    leaderboards = select(
        (workout.user_id, sum(workout.repetitions), sum(workout.weight)) for workout in UserExerciseData)

    return [{'username': _get_username(l[0]), 'reps': l[1], 'weights': l[2]} for l in leaderboards]


@db_session
def _get_user_id(username):
    """ Command to convert a username to user id

    :param username: (str) The username of the account
    :return: The integer user ID associated with the account
    """
    user_id = select(u.user_id for u in UserInformationData if u.username == username).first()

    return user_id


@db_session
def _get_username(user_id):
    """
    Command to convert user id to username
    :param user_id: The integer user ID associated with the account
    :return: (str) The username of the account
    """
    username = select(u.username for u in UserInformationData if u.user_id == user_id).first()

    return username


@db_session
def _get_workout_id(username):
    """ Command to convert a username to workout_id

    :param username: (str) The username of the account
    :return: The integer workout ID associated with the account
    """
    workout_id = select(u.current_workout_id for u in UserInformationData if u.username == username).first()

    return workout_id
