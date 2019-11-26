

class Action(object):
	def __init__(self):
		self.triggers = []
		self.effects = []
	
	def addTrigger(self, trigger):
		self.triggers.append(trigger)
	
	def getTriggers(self):
		return self.triggers
		
	def addEffect(self, effect):
		self.effects.append(effect)
	
	def getEffects(self):
		return self.effects
	