class ourCalendar:
	"""Represents a calendar ics"""

	def __init__(self):
		self.events = "BEGIN:VCALENDAR\nVERSION:2.0\n"

	def addEvent(self, event):
		self.events+=event+"\n"

	def output(self):
		self.events+="END:VCALENDAR\n"
		return self.events


