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
