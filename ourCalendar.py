from datetime import datetime
from dateutil import tz

class ourCalendar:
	"""Represents a calendar .ics"""

	def __init__(self):
		# string that will be written to .ics
		self.events = "BEGIN:VCALENDAR\nVERSION:2.0\n"

	def add_event(self, event):
		self.events += event + "\n"

	def write_file(self, file_name):
		# writes to a .ics file
		self.events+="END:VCALENDAR\n"
		with open(file_name, 'w') as f:
			f.write(self.events)

	def read_calendar(self, orig_file):
		# returns a list of events where each event is a dictionary
		# example: [{'name': ..., 'to': ..., 'from': ...,  'at':..., 'with':...}, {'name': ..., 'to': ..., 'from': ...,  'at':..., 'with':...}, ...]
		event_list = [] 
		with open(orig_file, 'r') as f:
			i = 0
			for line in f:
				if(line.startswith('BEGIN:VEVENT')):
					event_list.append({})
				if(line.startswith('DTSTART')):
					info = line.split(":")
					time = datetime.strptime(info[1].rstrip(), '%Y%m%dT%H%M%SZ')
					from_zone = tz.tzutc()
					to_zone = tz.tzlocal()
					time = time.replace(tzinfo=from_zone)
					time = time.astimezone(to_zone)
					event_list[i]["from"] = time
				if(line.startswith('DTEND')):
					info = line.split(":")
					time = datetime.strptime(info[1].rstrip(), '%Y%m%dT%H%M%SZ')
					from_zone = tz.tzutc()
					to_zone = tz.tzlocal()
					time = time.replace(tzinfo=from_zone)
					time = time.astimezone(to_zone)
					event_list[i]["to"] = time
				if(line.startswith('DESCRIPTION')):
					info = line.split(":")
					if(info[1].rstrip()):
						event_list[i]["with"] = info[1].rstrip()
					else:
						event_list[i]["with"] = ""
				if(line.startswith('LOCATION')):
					info = line.split(":")
					if(info[1].rstrip()):
						event_list[i]["at"] = info[1].rstrip()
					else:
						event_list[i]["at"] = ""
				if(line.startswith('SUMMARY')):
					info = line.split(":")
					event_list[i]["event_title"] = info[1].rstrip()
				if(line.startswith('END:VEVENT')):
					i = i+1
		return event_list







