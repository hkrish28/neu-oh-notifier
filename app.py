import requests
import time
import json
import os
from config import LOGIN_URL, MONITOR_URL, COURSE_ID, USER, PASSWORD, REDIRECT_URL, CONNECTOR_URL, TEAMS_WEBHOOK_ENABLED
from playsound import playsound

def send_notification(message):
    if TEAMS_WEBHOOK_ENABLED == 'True':
        send_message_to_teams_webhook(message)
    command = f'display notification "{message}" with title OH Queue Update'
    playsound('notification.mp3')
    os.system('osascript -e \'' + command + '\'')
    
def send_message_to_teams_webhook(message):
    headers = {'Content-Type': 'application/json'}
    payload = {
        "text": message
    }
    response = requests.post(CONNECTOR_URL, headers=headers, data=json.dumps(payload))
    
    if response.status_code == 200:
        print("Message sent successfully to Microsoft Teams!")
    else:
        print("Failed to send message to Microsoft Teams. Status code:", response.status_code)


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
    errorCounter = 0
    # Start a session
    with requests.Session() as session:
        auth_token = fetch_auth_token(session)
        send_message_to_teams_webhook("Monitoring started. You will be notified when the queue size changes.")
        while True:
            try:
                # Fetch the webpage after login
                response = session.get(MONITOR_URL + str(COURSE_ID), headers={'Cookie': 'auth_token=' + auth_token}) 
                
                if response.status_code == 401:  # Unauthorized, refresh token
                    print("Unauthorized. Refreshing token...")
                    errorCounter += 1
                    auth_token = fetch_auth_token(session)
                    continue

                queue_size = json.loads(response.content).get('queues')[0].get('queueSize')

                if queue_size == 0 :
                    print("Queue size 0. Waiting...")
                else:
                    # Queue size changed, send notification and update the queue size
                    print("Notification to be sent. Queue size is now: ", queue_size)
                    send_notification("OH Queue Update", "Queue size is now: " + str(queue_size))
                errorCounter = 0
                time.sleep(60)  # Adjust this value as needed
            except Exception as e:
                auth_token = fetch_auth_token(session)
                print("Error:", e)
                print("Response:", response.content)
                if errorCounter >= 3:
                    send_notification("Error occurred. Check console for details.")
                time.sleep(20)  # Wait before retrying

# Start the login and monitoring process
login_and_check_changes()