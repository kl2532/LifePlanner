import event as e
import ourCalendar as c
from datetime import datetime
from dateutil import tz

#declaring a calendar
cal = c.ourCalendar()
# Read original Calendar
orig_event_dict = cal.readCalendar('my.ics') # [{'name': ..., 'to': ..., 'from': ...,  'at':..., 'with':...}, {'name': ..., 'to': ..., 'from': ...,  'at':..., 'with':...}, ...]
for orig_e in orig_event_dict:
	e_name = orig_e['name']
	e_to = orig_e['to']
	e_from = orig_e['from']
	e_at = orig_e['at']
	e_with = orig_e['with']
	orig_event = e.Event(e_name, e_from, e_to, e_at, e_with)
	cal.addEvent(orig_event.create_string_event())

#Event 1
begin = datetime.strptime('2015-01-02 02:30:40', '%Y-%m-%d %H:%M:%S')
end = datetime.strptime('2015-01-02 03:00:40', '%Y-%m-%d %H:%M:%S')
event = e.Event("Wake", begin, end, "Hungarian", "Suna")
cal.addEvent(event.create_string_event())
# Event 2
begin2 = datetime.strptime('2015-01-02 05:30:40', '%Y-%m-%d %H:%M:%S')
end2 = datetime.strptime('2015-01-02 06:00:40', '%Y-%m-%d %H:%M:%S')
event2 = e.Event("Wake2", begin2, end2, "Hungarian", "Suna")
cal.addEvent(event2.create_string_event())
# Write a .ics file
cal.write_file('new.ics')

# UID and DTSTAMP are unique for each event
