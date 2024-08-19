from google.oauth2 import service_account
from googleapiclient.discovery import build

credentials = service_account.Credentials.from_service_account_file(
    'credentials/service-account-file.json',
    scopes=['https://www.googleapis.com/auth/calendar']
)
calendar_service = build('calendar', 'v3', credentials=credentials)

def create_appointment(summary, start_time, end_time):
    event = {
        'summary': summary,
        'start': {'dateTime': start_time, 'timeZone': 'America/Los_Angeles'},
        'end': {'dateTime': end_time, 'timeZone': 'America/Los_Angeles'},
    }
    event = calendar_service.events().insert(calendarId='primary', body=event).execute()
    return event

