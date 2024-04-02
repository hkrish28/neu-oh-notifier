# neu-oh-notifier

This is a simple project to get a desktop notification whenever there is a change to the active queue size for the course you are a teaching assistant for at Northeastern University(for courses that make use of Khoury Office Hours portal).

# Set up

- Install [Python3](https://www.python.org/downloads/)
- Run `pip install -r requirements.txt` to install the app dependencies
- Within config.py:
    - Update course id for the course (number that you see in the URL of your course office hours page)
    - If you would want to send notification to teams, create an incoming webhook within Teams [this way](https://learn.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook?tabs=newteams%2Cdotnet) and set CONNECTOR_URL to the webook url that got created. Also, set TEAMS_WEBHOOK_ENABLED to True.

# Running the app

Run `python3 app.py` in the project directory and the app will start running and notify you when there is any change to office hours queue. Enjoy!

Note: When you run the application for the first time, you will be prompted to enter your username, password (that you use for logging into the Khoury Admin portal).