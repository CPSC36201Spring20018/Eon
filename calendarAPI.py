from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import datetime

birthdays = '1p41h2gbd7op5gkvr4breqo3u0@group.calendar.google.com'
HVAC = '430r6sggfr9beuvufq1463sosg@group.calendar.google.com'
work = 'kmtkco94hncfn4dhlfg9h8smu8@group.calendar.google.com'

SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('calendar', 'v3', http=creds.authorize(Http()))

now = datetime.datetime.utcnow().isoformat() + 'Z'
print('Getting the upcoming 5 events')
events_result = service.events().list(calendarId= HVAC, timeMin=now,
				      maxResults=5, singleEvents=True,
				      orderBy='startTime').execute()
events = events_result.get('items', [])

if not events:
    print('No upcoming events found.')
for event in events:
    start = event['start'].get('dateTime', event['start'].get('date'))
    print(start, event['summary'])
