from database import init_development_db, get_exercise

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
    assert(correct == output)


