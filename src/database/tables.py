from pony.orm import *


# The database variable to be used across DBS.
DATABASE = Database()


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
    DATABASE.bind(
        provider='sqlite',
        filename='dev-database.sqlite',
        create_db=True)
    DATABASE.generate_mapping(create_tables=True)
