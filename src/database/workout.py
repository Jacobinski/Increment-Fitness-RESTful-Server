from pony.orm import *
from exercise import UserInformationData1, UserExerciseData1

# Generate a database variable which represents our MySQL database.
db = Database()


class UserWorkoutData1(db.Entity):
    """Python representation of User Workout Data Table
    """
    workout_id = PrimaryKey(int, size=32)
    user_id = Required(int)
    title = Required(str)
    date = Required(int, size=32)


@db_session
def add_workout(user_id, title, date):
    """Command to add workout to SQL table

    :param user_id: (int) The user ID who did the workout.
    :param title: (str) The name of the workout.
    :param date: (int) The epoch time associated with the end of the workout.
    :return: workout_id: (int) The unique ID of the workout.
    """
    # Add a new entry to the UserWorkoutData table
    max_workout_id = select(max(u.workout_id) for u in UserWorkoutData1 if user_id == u.user_id).first()
    UserWorkoutData1(
        workout_id=max_workout_id+1,
        user_id=user_id,
        title=title,
        date=date
    )

    # Update the UserInfoTable to reflect this new information
    user = UserInformationData1.get(user_id=user_id)
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
    workout = UserWorkoutData1.get(workout_id=workout_id)
    workout.set(title=title, date=date)


@db_session
def get_workout(workout_id):
    """Command to update a workout in the SQL table

    :param workout_id: (int) The unique ID of the workout.
    :return: An array of rows from the SQL table
    """
    exercise = select(e for e in UserExerciseData1 if e.workout_id == workout_id)[:]
    exercise = [e.to_dict() for e in exercise]
    return exercise


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
