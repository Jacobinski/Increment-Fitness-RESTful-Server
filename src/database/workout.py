from pony.orm import *
from tables import UserInformationData, UserExerciseData, UserWorkoutData


@db_session
def add_workout(user_id, title, date):
    """Command to add workout to SQL table

    :param user_id: (int) The user ID who did the workout.
    :param title: (str) The name of the workout.
    :param date: (int) The epoch time associated with the end of the workout.
    :return: workout_id: (int) The unique ID of the workout.
    """
    # Add a new entry to the UserWorkoutData table
    max_workout_id = select(max(u.workout_id) for u in UserWorkoutData if user_id == u.user_id).first()
    UserWorkoutData(
        workout_id=max_workout_id+1,
        user_id=user_id,
        title=title,
        date=date
    )

    # Update the UserInfoTable to reflect this new information
    user = UserInformationData.get(user_id=user_id)
    user.set(current_workout_id=max_workout_id+1)

    return max_workout_id+1


@db_session
def update_workout(workout_id, title, date):
    """Command to update a workout in the SQL table

    :param workout_id: (int) The unique ID of the workout.
    :param title: (str) The name of the workout.
    :param date: (int) The epoch time associated with the end of the workout.
    :return: None
    """
    workout = UserWorkoutData.get(workout_id=workout_id)
    workout.set(title=title, date=date)


@db_session
def get_workout(workout_id):
    """Command to get a workout from the SQL table

    :param workout_id: (int) The unique ID of the workout.
    :return: An array of rows from the SQL table
    """
    def _format_output(exercise_data, workout_data):
        output = {}
        exercise_data = [d.to_dict() for d in exercise_data]
        workout_data = workout_data.to_dict()

        # Format workout information
        output['title'] = workout_data['title']
        output['date'] = workout_data['date']

        # Format exercise information
        for e in exercise_data:
            name = e['exercise']

            # Append information to existing exercise entry if available
            if name in output:
                e_dict = output[name]
                e_dict['weights'].append(e['weight'])
                e_dict['reps'].append(e['repetitions'])
                e_dict['start_times'].append(e['start_time'])
                e_dict['end_times'].append(e['end_time'])
            # Else create new exercise entry
            else:
                output[name] = {
                    'reps': [e['weight']],
                    'weights': [e['repetitions']],
                    'start_times': [e['start_time']],
                    'end_times': [e['end_time']]
                }
        return output

    # Obtain and sort exercises
    exercise = select(e for e in UserExerciseData if e.workout_id == workout_id)[:]
    workout = UserWorkoutData.get(workout_id=workout_id)
    exercise = _format_output(exercise, workout)

    return exercise
