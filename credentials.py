import json
import getpass
import base64

def encode_credentials(username, password):
    encoded_username = base64.b64encode(username.encode()).decode()
    encoded_password = base64.b64encode(password.encode()).decode()
    return encoded_username, encoded_password

def decode_credentials(encoded_username, encoded_password):
    username = base64.b64decode(encoded_username.encode()).decode()
    password = base64.b64decode(encoded_password.encode()).decode()
    return username, password


def promptCredentials():
    print("Please provide your username and password.")
    username = input("Username: ")
    password = getpass.getpass("Password: ")
    remember_credentials = input("Do you want to remember the credentials? This will store the encoded credentials in your project root. (y/n): ").lower()
    
    if remember_credentials in ['y', 'yes', 'true', '1']:
        encoded_username, encoded_password = encode_credentials(username, password)
        with open('creds.json', 'w') as f:
            json.dump({'username': encoded_username, 'password': encoded_password}, f)
        print("Credentials saved.")
    else:
        print("Credentials not saved.")

    return username, password


def get_credentials(forcePrompt=False):
    if forcePrompt:
        return promptCredentials()

    try:
        with open('creds.json', 'r') as f:
            creds = json.load(f)
            return decode_credentials(creds['username'], creds['password'])
    except FileNotFoundError:
        return promptCredentials()
