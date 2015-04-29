from datetime import datetime
from dateutil import tz
import uuid

class Event:
	"""Represents a calendar ics"""
	def __init__(self, name, begin, end, location, person):
		self.name = name
		self.begin = begin
		self.end = end
		self.location = location
		self.person = person

	def createEvent(self):
		x = ""
		x = x + "BEGIN:VEVENT\n"
		to_zone = tz.tzutc()
		from_zone = tz.tzlocal()
		self.begin = self.begin.replace(tzinfo=from_zone)
		self.begin = self.begin.astimezone(to_zone)
		self.end = self.end.replace(tzinfo=from_zone)
		self.end = self.end.astimezone(to_zone)

		x = x + "DTSTAMP:20151231T000000Z\n"
		x = x + "DTSTART:" + self.begin.strftime("%Y%m%dT%H%M%SZ")+ '\n'
		x = x + "DTEND:" + self.end.strftime("%Y%m%dT%H%M%SZ") + '\n'
		x = x + "SUMMARY:" + self.name + '\n'
		x = x + "DESCRIPTION:" + "with " + self.person + '\n'
		x = x + "LOCATION:" + self.location + '\n'
		x = x + "UID:" + str(uuid.uuid1()) + '\n'
		x = x + "END:VEVENT"
		return x