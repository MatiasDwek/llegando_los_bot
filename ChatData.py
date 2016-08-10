class ScheduleTime(object):
	hour = 12
	minute = 0
	
	@staticmethod
	def validate_time(hour, minute):
		if (hour in range(0, 24)) and (minute in range(0, 60)):
			return True;
		else:
			return False;

class ChatData(object):
	schedule_active = True
	schedule_modulo = 1
	
	def __init__(self):
		self.schedule_time = ScheduleTime()
	
	@staticmethod
	def validate_modulo(modulo):
		if (modulo in range(1, 32)):
			return True;
		else:
			return False;
	