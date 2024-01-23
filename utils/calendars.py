from pprint import pprint
# from google import Create_Service
from googleapiclient.discovery import build

CLIENT_SECRET_FILE ='client_secret_1003524504215-1hfq4qk0ljcng12vstc838ig0d3l9md4.apps.googleusercontent.com.json'
API_NAME='calendar'
API_VERSION='v3'
SCOPES=['https://www.googleapis.com/auth/calendar']

service = build(CLIENT_SECRET_FILE, API_NAME,API_VERSION,SCOPES)

# to create 
request = {
    'summary':'New date set'
}

response = service.calendars().insert(body=request).execute()