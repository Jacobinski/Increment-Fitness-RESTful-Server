Increment Database Repository
=============================
[![Build Status](https://travis-ci.com/Jacobinski/inc-dbs.svg?token=NEDcUSneGHwPvWA1oiYU&branch=master)](https://travis-ci.com/Jacobinski/inc-dbs)

What's Here
-----------

This sample includes:

* README.md - this file
* appspec.yml - this file is used by AWS CodeDeploy when deploying the web
  application to EC2
* requirements.txt - this file is used install Python dependencies needed by
  the Flask application
* scripts/ - this directory contains scripts used by AWS CodeDeploy when
  installing and deploying your application on the Amazon EC2 instance
* src/ - this directory contains the Python source code for the Flask app


Getting Started
---------------
Clone the project's repository to your local computer. We will setup a
virtual environment for developing on this project, then run the application.

1. Create a Python virtual environment for the  project. This virtual
   environment allows you to isolate this project and install any packages you
   need without affecting the system Python installation. At the terminal, type
   the following command:

        $ virtualenv .venv

2. Activate the virtual environment (python 2.7):

        $ activate ./venv/bin/activate

3. Install Python dependencies for this project:

        $ pip install -r requirements.txt

4. Start the Flask development server:

        $ python src/application.py --port 8000 --debug

5. Open http://127.0.0.1:8000/ in a web browser to view the output of your
   service.

Production
----------
To run the production Flask server, run the application with no args

        $ python src/application.py

Testing
-------
To test any of the functionality of this code, we can run the development server locally, and issue curl commands to GET, POST, PATCH, etc.
Alternatively, we could run the Python unit testing framework with a clean dev database

        $ Pytest

API - Exercise
--------------
The endpoint for exercise data is **/api/exercises/**. The user may either post
exercise data, or get exercise data.

#### POST

This command will add an exercise to the database.
* Inputs:
    * user_id: (int) The user ID who did the workout.
    * start_time: (int) The workout's start time in epoch.
    * end_time: (int) The workout's end time in epoch.
    * repetitions: (int) The number of repetitions in the set.
    * weight: (int) The weight of the set in kilograms.
    * exercise: (str) The string name of the activity.
    * variant: (str) The variant of the activity. Left hand, right hand, etc.
    * skeleton_data: (bytes) A binary file for the skeleton activity file.

* Example

        $ curl -v 0.0.0.0:8000/api/exercises -X POST -F "user_id=0" -F "start_time=5" -F "end_time=6" -F "repetitions=6" -F "weight=9" -F "exercise=Squat" -F "variant=None" -F "skeleton_data=@test_image.jpg"

* Sample Output

        {
            "data": null,
            "message": "Successful POST to exercise table",
            "status": 200
        }

#### GET

This command will get a user's exercise from the database.

* Inputs:
    * username: (str) The user whose data we will fetch.
    * month: (int) The month of data to obtain in MM format.
    * year: (int) The month of data to obtain in YYYY format.

* Example

        $ curl -v 0.0.0.0:8000/api/exercises -X GET -d "username=Baratheon" -d "month=03" -d "year=2018"

* Sample Output

      {
      "data": {
        "data": [
          {
            "date": 1521934535,
            "exercises": {
              "endTimes": [
                1521934538
              ],
              "exercise": "Squat",
              "reps": [
                5
              ],
              "startTimes": [
                1521934535
              ],
              "weights": [
                0
              ]
            }
          },
          {
            "date": 1521934536,
            "exercises": {
              "endTimes": [
                1521934538
              ],
              "exercise": "Bicep Curl",
              "reps": [
                5
              ],
              "startTimes": [
                1521934536
              ],
              "weights": [
                10
              ]
            }
          },
          {
            "date": 1522178404,
            "exercises": {
              "endTimes": [
                1522178418
              ],
              "exercise": "BicepCurl",
              "reps": [
                10
              ],
              "startTimes": [
                1522178404
              ],
              "weights": [
                7
              ]
            }
          }
        ],
        "username": "Baratheon"
      },
      "message": "Successful GET of page",
      "status": 200


API - Leaderboard
-----------------
This endpoint is located at **/api/leaderboards/**

#### GET

This command will get the number of reps and weights that each user has lifted.

* Inputs:
    * Nothing

* Example

        $ curl -v 0.0.0.0:8000/api/leaderboards -X GET

* Sample Output

        {
          "data": [
            {
              "reps": 26,
              "username": "Baratheon",
              "weights": 26
            },
            {
              "reps": 103,
              "username": null,
              "weights": 94
            },
            {
              "reps": 5,
              "username": null,
              "weights": 10
            },
            {
              "reps": 5,
              "username": null,
              "weights": 10
            },
            {
              "reps": 108,
              "username": null,
              "weights": 96
            },
            {
              "reps": 39,
              "username": "Stark",
              "weights": 49
            },
            {
              "reps": 10,
              "username": "Lannister",
              "weights": 12
            },
            {
              "reps": 9,
              "username": "Greyjoy",
              "weights": 4
            }
          ],
          "message": "Successful GET of page",
          "status": 200
        }

API - Workout
-------------
This endpoint is located at **/api/workouts/**

#### POST

This command will add a workout to the database. Returns the id of the new workout.

* Inputs:
    * user_id: (int) The user ID who did the workout.
    * title: (str) The name of the workout.
    * (int) The epoch time associated with the end of the workout.

* Example

        $ curl -v 0.0.0.0:8000/api/workouts -X POST -d "date=12345678" -d "user_id=0" -d "title=Awesome Workout"

* Sample Output

        {
          "data": {
            "New_workout_id": 8
          },
          "message": "Successful POST to workout table",
          "status": 200
        }


#### GET

This command will get a workout from the database.

* Inputs:
    * workout_id: (int) The unique ID of the workout.
    * title: (str) The name of the workout.
    * (int) The epoch time associated with the end of the workout.

* Example

        $ curl -v 0.0.0.0:8000/api/workouts -X GET -d "workout_id=1"

* Sample Output

        {
          "data": {
            "Squat": {
              "end_times": [
                1522208404
              ],
              "reps": [
                35
              ],
              "start_times": [
                1522208304
              ],
              "weights": [
                25
              ]
            },
            "date": 1522208325,
            "title": "Targaryen Workout"
          },
          "message": "Successful GET of page",
          "status": 200
        }


#### PATCH

This command will update a workout in the datase.

* Inputs:
    * workout_id: (int) The unique ID of the workout.
    * title: (str) The name of the workout.
    * (int) The epoch time associated with the end of the workout.

* Example

        $ curl -v 0.0.0.0:8000/api/workouts -X PATCH -d "date=111111" -d "workout_id=1" -d "title=Alright Workout"

* Sample Output

        {
          "data": {
            "date": 111111,
            "title": "Alright Workout",
            "user_id": 11111115,
            "workout_id": 1
          },
          "message": "Successful PATCH of page",
          "status": 200
        }


API - User
----------
This endpoint is located at **/api/user/**


#### GET

This command will get all workout ids associated with a username.

* Inputs:
    * username: (str) The user whose workouts are retrieved.

* Example

        $ curl -v 0.0.0.0:8000/api/user -X GET -d "username=Baratheon"

* Sample Output:

        {
          "data": {
            "Workouts": [
              0,
              4
            ]
          },
          "message": "Successful GET of page",
          "status": 200
        }


API - Users
-----------
This endpoint is located at **/api/users/**

#### GET

This command will get information about all users in the database.

* Inputs:
    * None

* Example

        $ curl -v 0.0.0.0:8000/api/users -X GET

* Sample Output

        {
          "data": [
            {
              "current_workout_id": 8,
              "user_id": 0,
              "username": "Baratheon"
            },
            {
              "current_workout_id": 1,
              "user_id": 11111115,
              "username": "Targaryen"
            },
            {
              "current_workout_id": 2,
              "user_id": 22222220,
              "username": "Stark"
            },
            {
              "current_workout_id": 3,
              "user_id": 33333335,
              "username": "Lannister"
            },
            {
              "current_workout_id": 4,
              "user_id": 44444440,
              "username": "Greyjoy"
            }
          ],
          "message": "Successful GET of page",
          "status": 200
        }


Setup
-----
To avoid PyCharm from not properly locating certain includes, right click "src" and select Mark Directory as Sources Root.

External Database Access
------------------------
Access the database through external SQL database software using the following
configurations:

**Host:** increment.cx9kpie1sol8.us-west-1.rds.amazonaws.com

**Username:** admin

**Password:** L69VLKJTEwgJVBHNBt

**Port:** 3306
