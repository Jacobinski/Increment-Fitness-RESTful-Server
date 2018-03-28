from database import *

# NOTE: The database should have been initialized in test_exercise


def test_get_workout():
    correct = {'date': 1522208304,
               u'Squat':
                   {'start_times': [1522208309],
                    'weights': [5],
                    'reps': [0],
                    'end_times': [1522208367]},
               u'Sit ups':
                   {'start_times': [1522208317],
                    'weights': [3],
                    'reps': [3],
                    'end_times': [1522208327]},
               u'Deadlift':
                   {'start_times': [1522208307, 1522208308],
                    'weights': [5, 10],
                    'reps': [5, 10],
                    'end_times': [1522208367, 1522208367]},
               'title': u'My First Workout'
               }
    output = get_workout(workout_id=0)

    assert(output == correct)


def test_update_workout():
    correct = {'date': 1522208555, 'user_id': 0, 'workout_id': 0, 'title': u'My Last Workout'}
    output = update_workout(workout_id=0, title="My Last Workout", date=1522208555)

    assert(output == correct)


def test_add_workout():
    correct1 = {'New_workout_id': 2}
    correct2 = {'date': 1522208765, 'title': u'Boring Workout Title'}
    output1 = add_workout(user_id=0, title="Boring Workout Title", date=1522208765)
    output2 = get_workout(workout_id=output1['New_workout_id'])

    assert(output1 == correct1)
    assert(output2 == correct2)
