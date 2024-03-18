import requests
import time
import json
import os
from config import LOGIN_URL, MONITOR_URL, COURSE_ID, USER, PASSWORD, REDIRECT_URL

def send_notification(title, message):
    command = f'display notification "{message}" with title "{title}"'
    os.system('osascript -e \'' + command + '\'')
    
# URL of the login page and the page to monitor


def fetch_auth_token(session):
    # Perform login
    login_data = {
        "username": USER,
        "password": PASSWORD,
        "code": ""
    }
    response = session.post(LOGIN_URL, json=login_data)
    token = json.loads(response.content).get('key')
    response = session.post(REDIRECT_URL, headers = {'Authorization': 'Token ' + token})
    auth_token = json.loads(response.content).get('redirect').split("=")[1]
    return auth_token


# Function to log in and check for changes
def login_and_check_changes():
    # Start a session
    with requests.Session() as session:
        auth_token = fetch_auth_token(session)
        queue_size = -1 # Initialize queue size to an invalid number so that first check will always trigger a notification
        while True:
            try:
                # Fetch the webpage after login
                response = session.get(MONITOR_URL + str(COURSE_ID), headers={'Cookie': 'auth_token=' + auth_token}) 
                queue_size_latest = json.loads(response.content).get('queues')[0].get('queueSize')
                
                if response.status_code == 401:  # Unauthorized, refresh token
                    auth_token = fetch_auth_token(session)
                    continue

                if queue_size_latest == queue_size:
                    print("Queue size unchanged. Waiting...")
                    time.sleep(60)  # Adjust this value as needed
                else:
                    queue_size = queue_size_latest
                    # Queue size changed, send notification and update the queue size
                    print("Notification to be sent. Queue size is now: ", queue_size)
                    # Send a simple notification
                    send_notification("OH Queue Update", "Queue size is now: " + str(queue_size))
            except Exception as e:
                auth_token = fetch_auth_token(session)
                print("Error:", e)
                print("Response:", response.content)
                send_notification("OH Queue Update", "Error occurred. Check console for details.")
                time.sleep(10)  # Wait before retrying

# Start the login and monitoring process
login_and_check_changes()