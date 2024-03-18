# neu-oh-notifier

This is a simple project to get a desktop notification whenever there is a change to the active queue size for the course you are a teaching assistant for at Northeastern University(for courses that make use of Khoury Office Hours portal).

# Set up

- Install [Python3](https://www.python.org/downloads/)
- Run `pip install -r requirements.txt` to install the app dependencies
- Enter your username, password (that you use for logging into the Khoury Admin portal) and course id for the course(that you see in the URL of your course office hours page)

# Running the app

Run `python3 app.py` in the project directory and the app will start running and notify you when there is any change to office hours queue. Enjoy!