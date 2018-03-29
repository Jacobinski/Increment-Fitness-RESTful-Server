from database import *
import StringIO
import pytest


# Initialize the developer database
init_development_db()

@pytest.fixture(scope="module")
def setup():
    clean_dev_database()


def test_get_exercise(setup):
    correct = {'username': 'Tester',
               'data':
                   [{'date': 1522208307,
                     'exercises':
                         {'picture': 'MDAxMTAwMTE=\n',
                          'startTimes': [1522208307, 1522208308],
                          'reps': [5, 10],
                          'endTimes': [1522208367, 1522208367],
                          'weights': [5, 10],
                          'exercise': u'Deadlift'}
                     },
                    {'date': 1522208309,
                     'exercises':
                         {'picture': 'MDAxMTAwMTE=\n',
                          'startTimes': [1522208309],
                          'reps': [5],
                          'endTimes': [1522208367],
                          'weights': [0],
                          'exercise': u'Squat'}}]
               }
    output = get_exercise(username='Tester', month=03, year=2018)
    print(output)
    assert(output == correct)


def test_add_exercise(setup):
    correct_1 = None
    correct_2 = {'username': 'Tester',
                 'data':
                     [{'date': 1522208307,
                       'exercises':
                           {'picture': 'MDAxMTAwMTE=\n',
                            'startTimes': [1522208307, 1522208308],
                            'reps': [5, 10],
                            'endTimes': [1522208367, 1522208367],
                            'weights': [5, 10],
                            'exercise': u'Deadlift'}},
                      {'date': 1522208309,
                       'exercises':
                           {'picture': 'MDAxMTAwMTE=\n',
                            'startTimes': [1522208309],
                            'reps': [5],
                            'endTimes': [1522208367],
                            'weights': [0],
                            'exercise': u'Squat'}},
                      {'date': 1522208317,
                       'exercises':
                           {'picture': 'WzI2NjMwNV0=\n',
                            'startTimes': [1522208317],
                            'reps': [3],
                            'endTimes': [1522208327],
                            'weights': [3],
                            'exercise': u'Sit ups'}}]
                 }
    output_1 = add_exercise(user_id=0,
                          start_time=1522208317,
                          end_time=1522208327,
                          repetitions=3,
                          weight=3,
                          exercise="Sit ups",
                          variant="None",
                          skeleton_data=StringIO.StringIO([01010101]))
    output_2 = get_exercise(username='Tester', month=03, year=2018)

    assert(output_1 == correct_1)
    assert(output_2 == correct_2)


def test_get_leaderboards(setup):
    correct = [{'username': u'Tester', 'weights': 18, 'reps': 23},
               {'username': u'Jacob', 'weights': 35, 'reps': 25}]
    output = get_leaderboards()

    assert(output == correct)
