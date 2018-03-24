Increment Database Repository
=============================

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

        $ python src/application.py --port 8000

5. Open http://127.0.0.1:8000/ in a web browser to view the output of your
   service.

Commands
--------
We test the POST functionality of this code by running the development server locally, and issuing a curl POST command
with the required POST information. Note that there has to be a unique user_id & start_time pairing for each POST.

    curl -v 0.0.0.0:8000/api/workouts -X POST -F "user_id=8" -F "start_time=5" -F "end_time=6" -F "repetitions=6" -F "weight=9" -F "exercise=Squat" -F "variant=None" -F "skeleton_data=@test_image.jpg"

We test the GET functionality of this code by running the development server locally, and issuing a curl GET command
with the required user_id.

    $ curl 0.0.0.0:8000/api/workouts -X GET -d "username=Jacobinski" -d "month=03" -d "year=2018"

We test the GET functionality of the get leaderboards api endpoint by running the following command.
    
    $ curl 0.0.0.0:8000/api/leaderboards 

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
