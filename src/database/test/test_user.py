from database import *
import pytest


@pytest.fixture(scope="module")
def setup():
    clean_dev_database()


def test_get_user_workouts(setup):
    correct1 = {'Workouts': [0]}
    correct2 = {'Workouts': [1]}
    output1 = get_user_workouts(username='Baratheon')
    output2 = get_user_workouts(username='Targaryen')

    print(output1)
    print(output2)

    assert (output1 == correct1)
    assert (output2 == correct2)


def test_get_users(setup):
    correct = [{'username': u'Baratheon', 'current_workout_id': 0, 'user_id': 0},
               {'username': u'Targaryen', 'current_workout_id': 1, 'user_id': 11111115},
               {'username': u'Stark', 'current_workout_id': 2, 'user_id': 22222220},
               {'username': u'Lannister', 'current_workout_id': 3, 'user_id': 33333335},
               {'username': u'Greyjoy', 'current_workout_id': 4, 'user_id': 44444440}]
    output = get_users()

    print(output)

    assert (output == correct)
