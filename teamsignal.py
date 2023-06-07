import ts3
import time
import subprocess
import gspread
import random
import os
from oauth2client.service_account import ServiceAccountCredentials

# Define the Google Sheet details
scope = ['https://www.googleapis.com/auth/spreadsheets.readonly']
credentials = ServiceAccountCredentials.from_json_keyfile_name('sa_key.json', scope)
spreadsheet_key = os.getenv('SPREADSHEET_KEY')
worksheet_name = 'users'

# teamspeak
teamspeak_ip = os.getenv('TEAMSPEAK_IP')

# signal
telephone_number = os.getenv('TELEPHONE_NUMBER')
recipient_number = os.getenv('RECIPIENT_NUMBER')

def get_user_message_mapping():
    # Authorize the API client
    client = gspread.authorize(credentials)

    # Open the Google Sheet
    sheet = client.open_by_key(spreadsheet_key)
    worksheet = sheet.worksheet(worksheet_name)

    # Get the values from the worksheet
    values = worksheet.get_all_values()

    # Construct the username-message mapping
    user_message_mapping = {}
    for row in values[1:]:
        if len(row) >= 2:
            username = row[0]
            event = row[1]
            message = row[2]

            if username not in user_message_mapping:
                user_message_mapping[username] = {}
            
            user_message_mapping[username][event] = message
            user_message_mapping[username][event] = message

    return user_message_mapping

# get user mapping
user_mapping = get_user_message_mapping()

def get_message(user: str, event: str):
    message = f"{user} has entered the Server"
    if event == 'leave':
        message = f"{user} has left the Server"

    if user in user_mapping:
        events_for_user = user_mapping[user]
        message_string = events_for_user[event]
        messages = message_string.split(',')
        random_item = random.choice(messages)
        message = random_item
    
    return message

def send_singal_message(message: str):
    # Modify this function to execute the desired command with the user data
    command = f'signal-cli -u {telephone_number} send -g {recipient_number} -m "{message}"'
    subprocess.call(command, shell=True)

def watch_teamspeak():
    with ts3.query.TS3Connection(teamspeak_ip, 11200) as ts3conn:
        # Keep track of the user list
        current_user_list = []
        initiated = False

        # Connect to the Teamspeak 3 server
        while True:
            ts3conn.use(sid=274794)
            response = ts3conn.clientlist()

            # Parse the response and extract user names
            updated_user_list = []
            for client in response:
                user_name = client['client_nickname']
                if user_name != 'Unknown':
                    updated_user_list.append(user_name)

            # Find users who entered the channel
            entered_users = list(set(updated_user_list) - set(current_user_list))
            if entered_users and initiated:
                print("Users entered the channel:")
                for user in entered_users:
                    message = get_message(user, 'enter')
                    print(message)
                    send_singal_message(message)

            # Find users who left the channel
            left_users = list(set(current_user_list) - set(updated_user_list))
            if left_users and initiated:
                print("Users left the channel:")
                for user in left_users:
                    message = get_message(user, 'leave')
                    print(message)
                    send_singal_message(message)

            # Update the current user list
            current_user_list = updated_user_list

            # Wait for some time before checking again (e.g., every 5 seconds)
            initiated = True
            time.sleep(5)

# Start watching the Teamspeak server
watch_teamspeak()