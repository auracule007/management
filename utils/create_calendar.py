import requests
from google_auth_oauthlib.flow import InstalledAppFlow
import googleapiclient.discovery
from google.oauth2 import service_account

def create_calendar(event_text):
  SCOPES = ["https://www.googleapis.com/auth/calendar"]
  SERVICE_ACCOUNT_FILE = "client_secret_1003524504215-1hfq4qk0ljcng12vstc838ig0d3l9md4.apps.googleusercontent.com.json"
  credentials = service_account.Credentials.from_service_account_file(
      SERVICE_ACCOUNT_FILE, scopes=SCOPES
  )
  service = googleapiclient.discovery.build("calendar", "v3", credentials=credentials)
  calendar = {
      "summary": event_text,
      "timeZone": "UTC",
      "conferenceProperties": {
      "allowedConferenceSolutionTypes": [
        "courseReminder"
      ]
  }  
  }
  created_calendar = service.calendars().insert(body=calendar).execute()
  print("Calendar created: %s" % created_calendar["id"])
  return created_calendar
