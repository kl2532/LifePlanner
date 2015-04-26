#from ics import Calendar, Event
import event as e
import ourCalendar as c
from datetime import datetime
from dateutil import tz

cal = c.ourCalendar()
begin = datetime.strptime('2015-01-01 02:30:40', '%Y-%m-%d %H:%M:%S')
end = datetime.strptime('2015-01-01 03:00:40', '%Y-%m-%d %H:%M:%S')
begin2 = datetime.strptime('2015-01-01 05:30:40', '%Y-%m-%d %H:%M:%S')
end2 = datetime.strptime('2015-01-01 06:00:40', '%Y-%m-%d %H:%M:%S')
event = e.Event("Wake", begin, end, "Hungarian", "Suna")
event2 = e.Event("Wake2", begin2, end2, "Hungarian", "Suna")
l = event.createEvent()
l2 = event2.createEvent()
cal.addEvent(l)
cal.addEvent(l2)

x = cal.output()

print x
with open('my.ics', 'w') as f:
	f.write(x)


# UID and DTSTAMP are unique for each event
