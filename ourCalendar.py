from datetime import datetime
from dateutil import tz

class ourCalendar:
	"""Represents a calendar ics"""

	def __init__(self):
		self.events = "BEGIN:VCALENDAR\nVERSION:2.0\n"

	def addEvent(self, event):
		self.events+=event+"\n"

	def write_file(self, file_name):
		# returns a string 
		self.events+="END:VCALENDAR\n"
		with open(file_name, 'w') as f:
			f.write(self.events)

	def readCalendar(self, orig_file):
		# returns a list of events where each event is a dictionary
		stuff = [] #[{"BEGIN:VEVENT...END:VEVNT"}, {"BEGIN:VEVENT...END:VEVNT"}, ...]
		i = 0
		with open(orig_file, 'r') as f:
			for line in f:
				if(line.startswith('BEGIN:VEVENT')):
					stuff.append({})
				if(line.startswith('DTSTART')):
					info = line.split(":")
					time = datetime.strptime(info[1].rstrip(), '%Y%m%dT%H%M%SZ')
					from_zone = tz.tzutc()
					to_zone = tz.tzlocal()
					time = time.replace(tzinfo=from_zone)
					time = time.astimezone(to_zone)
					stuff[i]["from"] = time
				if(line.startswith('DTEND')):
					info = line.split(":")
					time = datetime.strptime(info[1].rstrip(), '%Y%m%dT%H%M%SZ')
					from_zone = tz.tzutc()
					to_zone = tz.tzlocal()
					time = time.replace(tzinfo=from_zone)
					time = time.astimezone(to_zone)
					stuff[i]["to"] = time
				if(line.startswith('with')):
					info = line.split(":")
					if(info[1].rstrip().startswith('with')):
						stuff[i]["DESCRIPTION"] = info[1].rstrip()
					else:
						stuff[i]["DESCRIPTION"] = ""
				if(line.startswith('LOCATION')):
					info = line.split(":")
					stuff[i]["at"] = info[1].rstrip()
				if(line.startswith('SUMMARY')):
					info = line.split(":")
					stuff[i]["name"] = info[1].rstrip()
				if(line.startswith('END:VEVENT')):
					i = i+1
		print stuff
		return stuff







