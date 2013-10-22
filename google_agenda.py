#!/usr/bin/env python
"""
@author:    Matthias Feys (matthiasfeys@gmail.com), IBCN (Ghent University)
@date:      Tue Oct 22 20:05:01 2013

starting from the Google Quickstart example
"""

import httplib2
import os
import sys
import datetime

from apiclient import discovery
from oauth2client import file
from oauth2client import client
from oauth2client import tools


from apiclient.discovery import build
from oauth2client.client import OAuth2WebServerFlow

import httplib2

# CLIENT_SECRETS is name of a file containing the OAuth 2.0 information for this
# application, including client_id and client_secret. You can see the Client ID
# and Client secret on the APIs page in the Cloud Console:
# <https://cloud.google.com/console#/project/1011918119399/apiui>
CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), 'client_secrets.json')

# Set up a Flow object to be used for authentication.
# Add one or more of the following scopes. PLEASE ONLY ADD THE SCOPES YOU
# NEED. For more information on using scopes please see
# <https://developers.google.com/+/best-practices>.
FLOW = client.flow_from_clientsecrets(CLIENT_SECRETS,
  scope=[
      'https://www.googleapis.com/auth/calendar',
      'https://www.googleapis.com/auth/calendar.readonly',
    ],
    message=tools.message_if_missing(CLIENT_SECRETS))
# If the credentials don't exist or are invalid run through the native client
  # flow. The Storage object will ensure that if successful the good
  # credentials will get written back to the file.
storage = file.Storage('sample.dat')
credentials = storage.get()
if credentials is None or credentials.invalid:
    credentials = tools.run_flow(FLOW, storage)

  # Create an httplib2.Http object to handle our HTTP requests and authorize it
  # with our good Credentials.
http = httplib2.Http()
http = credentials.authorize(http)

# Construct the service object for the interacting with the Calendar API.
service = discovery.build('calendar', 'v3', http=http)

def makeEvent(event):
    try:
      event = {
          'summary': event['title'],
          'location': 'KLJ-lokaal',
          'start': {
              'dateTime': event['date'].isoformat('T')
              },
          'end': {
              'dateTime': (event['date']+datetime.timedelta(hours=4)).isoformat('T')
              },
          'description':event['description']
        }

      created_event = service.events().insert(calendarId='primary', body=event).execute()


    except client.AccessTokenRefreshError:
        print ("The credentials have been revoked or expired, please re-run"
      "the application to re-authorize")


def main(argv):

  try:
      event = {
          'summary': 'Appointment',
          'location': 'Somewhere',
          'start': {
              'dateTime': '2011-06-03T10:00:00.000-07:00'
              },
          'end': {
              'dateTime': '2011-06-03T10:25:00.000-07:00'
              }
        }

      created_event = service.events().insert(calendarId='primary', body=event).execute()


  except client.AccessTokenRefreshError:
    print ("The credentials have been revoked or expired, please re-run"
      "the application to re-authorize")


# For more information on the Calendar API you can visit:
#
#   https://developers.google.com/google-apps/calendar/firstapp
#
# For more information on the Calendar API Python library surface you
# can visit:
#
#   https://developers.google.com/resources/api-libraries/documentation/calendar/v3/python/latest/
#
# For information on the Python Client Library visit:
#
#   https://developers.google.com/api-client-library/python/start/get_started
if __name__ == '__main__':
  main(sys.argv)