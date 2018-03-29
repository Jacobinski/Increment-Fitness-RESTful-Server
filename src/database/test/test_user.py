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

    assert(output1 == correct1)
    assert(output2 == correct2)
