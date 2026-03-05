#!/usr/bin/env python3
"""
iCloud Calendar Add Event Script
Usage: python3 add_event.py "Event Title" "2026-03-06T10:00:00" "2026-03-06T11:00:00" "Description"
"""

import sys
import urllib.request
import base64
import uuid
from datetime import datetime

# iCloud Configuration
ICLOUD_EMAIL = "wangjintao1999@icloud.com"
ICLOUD_PASSWORD = "bntm-ffft-vwgf-iybk"
CALDAV_URL = "https://caldav.icloud.com"
# Calendar home path
CALENDAR_HOME = "/8132224793/calendars/home/"

def create_ics_event(title, start_time, end_time, description="", alarm_minutes=15):
    """Create iCalendar format event with alarm reminder"""
    uid = str(uuid.uuid4())
    dtstamp = datetime.now().strftime("%Y%m%dT%H%M%S")
    
    ics = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//OpenClaw//iCloud Calendar//EN
CALSCALE:GREGORIAN
METHOD:PUBLISH
BEGIN:VEVENT
UID:{uid}
DTSTAMP:{dtstamp}Z
DTSTART:{start_time.replace('-', '').replace(':', '')}Z
DTEND:{end_time.replace('-', '').replace(':', '')}Z
SUMMARY:{title}
DESCRIPTION:{description}
STATUS:CONFIRMED
SEQUENCE:0
BEGIN:VALARM
TRIGGER:-PT{alarm_minutes}M
ACTION:DISPLAY
DESCRIPTION:{title}
END:VALARM
BEGIN:VALARM
TRIGGER:-PT5M
ACTION:DISPLAY
DESCRIPTION:马上开始: {title}
END:VALARM
END:VEVENT
END:VCALENDAR"""
    
    return ics

def add_event_to_icloud(title, start_time, end_time, description=""):
    """Add event to iCloud Calendar via CalDAV"""
    
    auth = base64.b64encode(f"{ICLOUD_EMAIL}:{ICLOUD_PASSWORD}".encode()).decode()
    
    # Create ICS content
    ics_content = create_ics_event(title, start_time, end_time, description)
    
    # Generate event URL path - use calendar home
    uid = str(uuid.uuid4())
    event_path = f"{CALENDAR_HOME}{uid}.ics"
    
    # Create request
    req = urllib.request.Request(
        CALDAV_URL + event_path,
        method="PUT",
        headers={
            "Authorization": f"Basic {auth}",
            "Content-Type": "text/calendar; charset=utf-8",
            "If-None-Match": "*"
        },
        data=ics_content.encode('utf-8')
    )
    
    try:
        response = urllib.request.urlopen(req, timeout=30)
        print(f"✅ Event added successfully!")
        print(f"📅 Title: {title}")
        print(f"🕐 Time: {start_time} - {end_time}")
        if description:
            print(f"📝 Description: {description}")
        return True
    except urllib.error.HTTPError as e:
        print(f"❌ Error: {e.code} - {e.reason}")
        print(f"   {e.read().decode() if e.fp else ''}")
        return False

def parse_natural_language(time_str):
    """Parse natural language time to datetime"""
    from datetime import datetime, timedelta
    
    now = datetime.now()
    
    # Simple parsing for demo - can be enhanced
    time_str = time_str.lower().strip()
    
    # Handle "tomorrow"
    if 'tomorrow' in time_str:
        date = now + timedelta(days=1)
    # Handle "today"
    elif 'today' in time_str:
        date = now
    # Handle day names
    elif 'monday' in time_str: date = now + timedelta(days=(7 - now.weekday() + 0))
    elif 'tuesday' in time_str: date = now + timedelta(days=(7 - now.weekday() + 1))
    elif 'wednesday' in time_str: date = now + timedelta(days=(7 - now.weekday() + 2))
    elif 'thursday' in time_str: date = now + timedelta(days=(7 - now.weekday() + 3))
    elif 'friday' in time_str: date = now + timedelta(days=(7 - now.weekday() + 4))
    elif 'saturday' in time_str: date = now + timedelta(days=(7 - now.weekday() + 5))
    elif 'sunday' in time_str: date = now + timedelta(days=(7 - now.weekday() + 6))
    else:
        date = now
    
    # Extract time if present (simple extraction)
    import re
    time_match = re.search(r'(\d{1,2}):(\d{2})', time_str)
    if time_match:
        hour = int(time_match.group(1))
        minute = int(time_match.group(2))
    else:
        hour = 9
        minute = 0
    
    return date.replace(hour=hour, minute=minute, second=0, microsecond=0)

def main():
    if len(sys.argv) < 3:
        print(__doc__)
        print("\nQuick demo - adding test event:")
        # Demo add
        now = datetime.now()
        start = now + timedelta(hours=2)
        end = start + timedelta(hours=1)
        add_event_to_icloud(
            "测试日程 - Test Event",
            start.strftime("%Y-%m-%dT%H:%M:%S"),
            end.strftime("%Y-%m-%dT%H:%M:%S"),
            "这是通过 OpenClaw 添加的测试日程"
        )
        return
    
    title = sys.argv[1]
    start_time = sys.argv[2]
    end_time = sys.argv[3] if len(sys.argv) > 3 else None
    description = sys.argv[4] if len(sys.argv) > 4 else ""
    
    if not end_time:
        # Default 1 hour duration
        try:
            start_dt = datetime.fromisoformat(start_time.replace('T', ' '))
            end_dt = start_dt + timedelta(hours=1)
            end_time = end_dt.strftime("%Y-%m-%dT%H:%M:%S")
        except:
            end_time = start_time
    
    add_event_to_icloud(title, start_time, end_time, description)

if __name__ == "__main__":
    from datetime import timedelta
    main()