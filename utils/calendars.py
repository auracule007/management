from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
import datetime
import os
import googleapiclient.discovery

CLIENT_SECRET_FILE ='client_secret_1003524504215-1hfq4qk0ljcng12vstc838ig0d3l9md4.apps.googleusercontent.com.json'
API_NAME='calendar'
API_VERSION='v3'
SCOPES=['https://www.googleapis.com/auth/calendar']

# service = build(CLIENT_SECRET_FILE, API_NAME,API_VERSION,SCOPES)

# # to create 
# request = {
#     'summary':'New date set'
# }

# response = service.calendars().insert(body=request).execute()
token_path  = CLIENT_SECRET_FILE
def create_google_calendar_event(course_event):
        SCOPES = ['https://www.googleapis.com/auth/calendar']

        creds = None
        token_path ='' # Path to token.json file, should be writable

        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first time.
        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    CLIENT_SECRET_FILE, SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(token_path, 'w') as token:
                token.write(creds.to_json())

        service = googleapiclient.discovery.build('calendar', 'v3', credentials=creds)

        event = {
            'id': course_event.id,
            'user': course_event.user.username,
            'summary': course_event.event_text,
            'description': f'Course: {course_event.course.name}',
            'start': {
                'dateTime': course_event.start_date.isoformat(),
                'timeZone': 'UTC',
            },
            'end': {
                'dateTime': course_event.end_date.isoformat(),
                'timeZone': 'UTC',
            },
        }

        calendar_id = 'primary'  # Use 'primary' for the primary calendar of the authenticated user
        event = service.events().insert(calendarId=calendar_id, body=event).execute()
        return event['id']

