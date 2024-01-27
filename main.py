from datetime import datetime, timedelta
import os.path
import re

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = [
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/calendar.calendarlist",
]

CALENDAR_TO_USE = "Timetable"
NUM_WEEKS = 22


def convert_to_iso_format(time_str: str, day: str) -> str:
    """
    Converts a time string to ISO format"""
    try:
        input_time = datetime.strptime(time_str, "%I:%M%p")
        day_mapping = {
            "monday": 0,
            "tuesday": 1,
            "wednesday": 2,
            "thursday": 3,
            "friday": 4,
            "saturday": 5,
            "sunday": 6,
            "m": 0,
            "t": 1,
            "w": 2,
            "th": 3,
            "f": 4,
            "s": 5,
            "su": 6,
        }
        if day.lower() not in day_mapping.keys():
            raise ValueError

        current_dt = datetime.now()
        days_until_target_day = (
            day_mapping[day.lower()] - current_dt.weekday() + 7
        ) % 7
        target_dt = current_dt + timedelta(days=days_until_target_day)
        combined_dt = datetime.combine(target_dt.date(), input_time.time())
        return combined_dt.isoformat()
    except ValueError:
        return "Invalid time format"


def subtract_minutes_from_iso(iso_time, minutes_to_subtract):
    try:
        original_time = datetime.fromisoformat(iso_time)
        subtracted_time = original_time - timedelta(minutes=minutes_to_subtract)
        return subtracted_time.isoformat()
    except ValueError:
        return "Invalid ISO time format"


def split_string(input_str):
    letters, numbers = re.match(r"([a-zA-Z]+)", input_str), re.search(
        r"(\d+)$", input_str
    )
    return letters.group(1) if letters else None, numbers.group(1) if numbers else None


def auth():
    """Creates a Google Calendar API service object and outputs token.json"""
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds


def get_calendar_id(service, calendar_name):
    """Gets the calendar ID of the calendar to use"""
    calendar_list = service.calendarList().list().execute()
    if calendar_name not in [
        calendar["summary"] for calendar in calendar_list["items"]
    ]:
        print("Creating calendar", calendar_name, "as it does not exist")
        calendar = {
            "summary": calendar_name,
            "timeZone": "Asia/Dubai",
        }
        created_calendar = service.calendars().insert(body=calendar).execute()
        print(f"Created calendar: {created_calendar['summary']}")
        calendar_id = created_calendar["id"]
    else:
        print("Using", calendar_name)
        calendar_id = [
            calendar["id"]
            for calendar in calendar_list["items"]
            if calendar["summary"] == calendar_name
        ][0]
    return calendar_id


def create_event(
    service, calendar_id, summary, description, start_time, end_time, day, num_weeks
):
    event = {
        "summary": summary,
        "description": description,
        "start": {
            "dateTime": start_time,
            "timeZone": "Asia/Dubai",
        },
        "end": {
            "dateTime": end_time,
            "timeZone": "Asia/Dubai",
        },
        "recurrence": ["RRULE:FREQ=WEEKLY;COUNT=" + str(num_weeks)],
    }

    eventCreated = service.events().insert(calendarId=calendar_id, body=event).execute()
    return eventCreated


def create_bits_event(service, calendar_id, summary, description, days, num_weeks):
    try:
        days = days.split(" ")
        timeMap = {
            1: "7:30AM",
            2: "8:25AM",
            3: "9:20AM",
            4: "10:15AM",
            5: "11:10AM",
            6: "12:05PM",
            7: "1:00PM",
            8: "1:55PM",
            9: "2:50PM",
            10: "3:45PM",
        }
        days = [day.lower() for day in days]
        for day in days:
            new_day, new_time = split_string(day)
            print("for the day : ", new_day)

            if len(new_time) == 0:
                raise ValueError
            elif len(new_time) == 1:
                start_time = timeMap[int(new_time)]
                end_time = timeMap[int(new_time) + 1]
                iso_form_start_time = convert_to_iso_format(start_time, new_day)
                iso_form_end_time = convert_to_iso_format(end_time, new_day)
                iso_form_end_time = subtract_minutes_from_iso(iso_form_end_time, 5)
            else:
                start_time = timeMap[int(new_time[0])]
                end_time = timeMap[int(new_time[-1]) + 1]
                iso_form_start_time = convert_to_iso_format(start_time, new_day)
                iso_form_end_time = convert_to_iso_format(end_time, new_day)
                iso_form_end_time = subtract_minutes_from_iso(iso_form_end_time, 5)
            create_event(
                service,
                calendar_id,
                summary,
                description,
                iso_form_start_time,
                iso_form_end_time,
                new_day,
                num_weeks,
            )

    except ValueError:
        return "Invalid time format"


def main():
    if not os.path.exists("credentials.json"):
        print("credentials.json not found, please download it from Google Cloud")
        input("Press enter to exit")
    print("Welcome to calendar creator")
    print()
    print("Press enter to use default values")
    print()
    print(
        "If you get Somthing is wrong error, please copy the link and paste it in an ignito window and login with your email"
    )
    print()
    creds = auth()

    try:
        service = build("calendar", "v3", credentials=creds)

        # get calendar id
        calender_to_use = input(
            f"Enter the name of the calendar to use (default: {CALENDAR_TO_USE}): "
        )
        if calender_to_use == "":
            calender_to_use = CALENDAR_TO_USE
        calendar_id = get_calendar_id(service, CALENDAR_TO_USE)

        num_weeks = input(
            f"Enter the number of weeks to create events for (default: {NUM_WEEKS}): "
        )
        if num_weeks == "":
            num_weeks = NUM_WEEKS

        exit = False
        while not exit:
            summary = input("Enter the course title (268 - OPERATING SYSTEMS): ")
            description = input("Enter the description of the event (CS F372 - L2): ")
            days = input("Enter the days of the event (M3 T5 Th2 F1): ")
            if summary == "" or description == "" or days == "":
                print("One or more fields are empty, please try again")
            else:
                print("Creating events...")
                create_bits_event(
                    service,
                    calendar_id,
                    summary,
                    description,
                    days,
                    num_weeks,
                )
                print("Events created successfully")
            if input("Do you want to create another event? (Y/n): ") == "n":
                exit = True

    except HttpError as error:
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    main()
