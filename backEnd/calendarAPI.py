from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import datetime

birthdays = '1p41h2gbd7op5gkvr4breqo3u0@group.calendar.google.com'
HVAC = '430r6sggfr9beuvufq1463sosg@group.calendar.google.com'
work = 'kmtkco94hncfn4dhlfg9h8smu8@group.calendar.google.com'

def initialize_read():
    SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
    store = file.Storage('credentials.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
        creds = tools.run_flow(flow, store)
    return build('calendar', 'v3', http=creds.authorize(Http()))

def initialize_write():
    SCOPES = 'https://www.googleapis.com/auth/calendar'
    store = file.Storage('credential.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
        creds = tools.run_flow(flow, store)
    return build('calendar', 'v3', http=creds.authorize(Http()))

def list():
    service = initialize_read()
    page_token = None
    while True:
        events = service.events().list(calendarId=HVAC, pageToken=page_token).execute()
        for event in events['items']:
            print(event['start'].get('dateTime', event['start'].get('date')),event['summary'])
        page_token = events.get('nextPageToken')
        if not page_token:
            break

def delete(event):
    service = initialize_write()
    service.events().delete(calendarId=HVAC, eventId=event).execute()

def create(requested_temp, start, end, day):
    service = initialize_write()
    event = {
        'summary': '90',
        'start': {
            'dateTime': '2018-04-30T09:00:00-07:00',
            'timeZone': 'America/Los_Angeles',
        },
        'end': {
            'dateTime': '2018-04-30T09:30:00-07:00',
            'timeZone': 'America/Los_Angeles',
        },
        'recurrence': [
            'RRULE:FREQ=WEEKLY;DAY=MO'
        ],
        'reminders': {
            'useDefault': True,
        },
    }
    event = service.events().insert(calendarId=HVAC, body=event).execute()

def main():
    delete('35a4b7o9ksd400b5cafq5ci1qj')

if __name__ == '__main__':
    main()
