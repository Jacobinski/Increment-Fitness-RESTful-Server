from database import *
import pytest


@pytest.fixture(scope="module")
def setup():
    clean_dev_database()


def test_get_workout(setup):
    correct = {'date': 1522208304,
               u'Squat': {
                   'start_times': [1522208309],
                   'weights': [5],
                   'reps': [0],
                   'end_times': [1522208367]},
               u'Deadlift': {
                   'start_times': [1522208307, 1522208308],
                   'weights': [5, 10],
                   'reps': [5, 10],
                   'end_times': [1522208367, 1522208367]},
               'title': u'Baratheon Workout'}
    output = get_workout(workout_id=0)

    print(output)

    assert(output == correct)


def test_update_workout(setup):
    correct = {'date': 1522208555, 'user_id': 0, 'workout_id': 0, 'title': u'My Last Workout'}
    output = update_workout(workout_id=0, title="My Last Workout", date=1522208555)

    print(output)

    assert(output == correct)


def test_add_workout(setup):
    correct1 = {'New_workout_id': 5}
    correct2 = {'date': 1522208765, 'title': u'Boring Workout Title'}
    output1 = add_workout(user_id=0, title="Boring Workout Title", date=1522208765)
    output2 = get_workout(workout_id=output1['New_workout_id'])

    print(output1)
    print(output2)

    assert(output1 == correct1)
    assert(output2 == correct2)
