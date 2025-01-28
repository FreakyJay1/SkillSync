from googleapiclient.discovery import build
from google.oauth2 import service_account
from utils import is_weekday, is_valid_time_range
from models import Meeting

SCOPES = ['https://www.googleapis.com/auth/calendar']

SERVICE_ACCOUNT_FILE = 'google_calendar_credentials.json'

creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('calendar', 'v3', credentials=creds)

def create_calendar_event(meeting: Meeting):
    
    if not is_weekday(meeting.start_time):
        raise ValueError("Meeting must be on a weekday.")
    if not is_valid_time_range(meeting.start_time, meeting.end_time):
        raise ValueError("Meeting time must be between 07:00 and 17:00.")
    
    user_timezone = "Africa/Johannesburg"
    
    event = {
        'summary': f'Meeting with {meeting.peer_id}',
        'start': {
            'dateTime': meeting.start_time.isoformat(),
            'timeZone': user_timezone,
        },
        'end': {
            'dateTime': meeting.end_time.isoformat(),
            'timeZone': user_timezone,
        },
        'attendees': [],
    }
    
    try:
        event = service.events().insert(calendarId='primary', body=event).execute()
        print(f"Event created: {event.get('htmlLink')}")
        return event
    except Exception as e:
        print(f"An error occurred creating the calendar event: {e}")
        raise