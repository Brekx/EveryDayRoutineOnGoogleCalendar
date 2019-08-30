from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
SCOPES = ['https://www.googleapis.com/auth/calendar']

def auth():
    creds = None
    service = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('calendar', 'v3', credentials=creds)
    return service
def send(service, body):
    return service.events().insert(calendarId='5l3ppia0e2r8qjhcfbb87qr62o@group.calendar.google.com', body=body).execute()
def insertEvent(service, body, calendarId):
    return service.events().insert(calendarId=calendarId, body=body).execute()
def insertCalendar(service, body):
    return service.calendars().insert(body=body).execute()
def getCalendarList(service):
    return service.calendarList().list().execute()