from database import *

# NOTE: The database should have been initialized in test_exercise


def test_get_user_workouts():
    correct1 = {'Workouts': [0]}
    correct2 = {'Workouts': [1]}
    output1 = get_user_workouts(username='Tester')
    output2 = get_user_workouts(username='Jacob')

    assert(output1 == correct1)
    assert(output2 == correct2)
