from pony.orm import *
import StringIO


# The database variable to be used across DBS.
DATABASE = Database()
_is_dev_database = False


class UserExerciseData(DATABASE.Entity):
    """Python representation of User Exercise Data Table
    """
    user_id = Required(int)
    workout_id = Required(int, size=32)
    start_time = Required(int, size=32)
    end_time = Required(int, size=32)
    repetitions = Required(int, size=16)
    weight = Required(int, size=16)
    exercise = Required(str)
    variant = Required(str)
    skeleton_data = Optional(buffer)

    PrimaryKey(user_id, start_time)


class UserInformationData(DATABASE.Entity):
    """Python representation of User Information Data Table
    """
    username = PrimaryKey(str)
    user_id = Required(int, unique=True)
    current_workout_id = Required(int, unique=True)


class UserWorkoutData(DATABASE.Entity):
    """Python representation of User Workout Data Table
    """
    workout_id = PrimaryKey(int, size=32)
    user_id = Required(int)
    title = Required(str)
    date = Required(int, size=32)


def init_production_db():
    """ Initialize the database to use the production database

    :return: None
    """
    # TODO: Remove the hardcoded values. This isn't good software practice, but fixing it requires setting up AWS Parameter
    #       Store on each developer's machine and the cloud, which is going to be a ton of work.
    DATABASE.bind(
        provider='mysql',
        host='increment.cx9kpie1sol8.us-west-1.rds.amazonaws.com',
        user='admin',
        passwd='L69VLKJTEwgJVBHNBt',
        db='increment_db')
    DATABASE.generate_mapping(create_tables=True)


def init_development_db():
    """ Initialize the database to use the a local database file

    :return: None
    """
    global _is_dev_database
    DATABASE.bind(
        provider='sqlite',
        filename='dev-database.sqlite',
        create_db=True)
    DATABASE.generate_mapping(create_tables=True)
    _is_dev_database = True


def clean_dev_database():
    """ Wipe and refresh the developer database

    :return: Nothing
    """
    global _is_dev_database
    if _is_dev_database:
        # Wipe the database. Only do this for the development database
        DATABASE.drop_all_tables(with_all_data=True)
        DATABASE.create_tables()

        # Populate the database
        with db_session:
            UserInformationData(username="Tester", user_id=0, current_workout_id=0)
            UserInformationData(username="Jacob", user_id=1, current_workout_id=1)

            UserWorkoutData(workout_id=0, user_id=0, title="My First Workout", date=1522208304)
            UserWorkoutData(workout_id=1, user_id=1, title="Jacob's Workout", date=1522208324)

            UserExerciseData(user_id=0, workout_id=0, start_time=1522208307, end_time=1522208367, repetitions=5,
                             weight=5, exercise="Deadlift", variant="None", skeleton_data=buffer('00110011'))
            UserExerciseData(user_id=0, workout_id=0, start_time=1522208308, end_time=1522208367, repetitions=10,
                             weight=10, exercise="Deadlift", variant="None", skeleton_data=buffer('00110011'))
            UserExerciseData(user_id=0, workout_id=0, start_time=1522208309, end_time=1522208367, repetitions=5,
                             weight=0, exercise="Squat", variant="None", skeleton_data=buffer('00110011'))
            UserExerciseData(user_id=1, workout_id=1, start_time=1522208304, end_time=1522208404, repetitions=25,
                             weight=35, exercise="Squat", variant="None", skeleton_data=buffer('01010101'))
    else:
        raise Exception
