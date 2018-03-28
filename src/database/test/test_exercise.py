from database import *
import StringIO

# Initialize developer database for unit testing
# Note: This should be a clean version of the database
init_development_db()


def test_get_exercise():
    correct = {'username': 'Tester',
               'data':
                   [{'date': 1522208307,
                     'exercises':
                         {'picture': 'MAAwADEAMQAwADAAMQAxAA==\n',
                          'startTimes': [1522208307, 1522208308],
                          'reps': [5, 10],
                          'endTimes': [1522208367, 1522208367],
                          'weights': [5, 10],
                          'exercise': u'Deadlift'}
                     },
                    {'date': 1522208309,
                     'exercises':
                         {'picture': 'MAAwADEAMQAwADAAMQAxAA==\n',
                          'startTimes': [1522208309],
                          'reps': [5],
                          'endTimes': [1522208367],
                          'weights': [0],
                          'exercise': u'Squat'}}]
               }
    output = get_exercise('Tester', 03, 2018)
    print(output)
    assert(output == correct)


def test_add_exercise():
    correct_1 = None
    correct_2 = {'username': 'Tester',
                 'data':
                     [{'date': 1522208307,
                       'exercises':
                           {'picture': 'MAAwADEAMQAwADAAMQAxAA==\n',
                            'startTimes': [1522208307, 1522208308],
                            'reps': [5, 10],
                            'endTimes': [1522208367, 1522208367],
                            'weights': [5, 10],
                            'exercise': u'Deadlift'}},
                      {'date': 1522208309,
                       'exercises':
                           {'picture': 'MAAwADEAMQAwADAAMQAxAA==\n',
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
    output_2 = get_exercise('Tester', 03, 2018)

    assert(output_1 == correct_1)
    assert(output_2 == correct_2)
