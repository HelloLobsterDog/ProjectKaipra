
class ActionTrigger(object):
	def __init__(self, contents, requiredActions, checkedActions, lang):
		self.matchedText = contents
		self.requiredActions = []
		if requiredActions != None:
			self.requiredActions.extend(requiredActions)
		self.checkedActions = []
		if checkedActions != None:
			self.checkedActions.extend(checkedActions)
		self.lang = lang
		
	def __str__(self):
		requiredActionsText = ''
		if self.requiredActions:
			if len(self.requiredActions) > 1:
				self.requiredActionsText = ', requiredActions=["{}"]'.format('", "'.join(self.requiredActions))
			else:
				self.requiredActionsText = ', requiredActions="{}"'.format(self.requiredActions[0])
		checkedActionsText = ''
		if self.checkedActions:
			if len(self.checkedActions) > 1:
				self.checkedActionsText = ', checkedActions=["{}"]'.format('", "'.join(self.checkedActions))
			else:
				self.checkedActionsText = ', checkedActions="{}"'.format(self.checkedActions[0])
		return 'ActionTrigger<matchedText="{}", lang={}{}{}>'.format(self.matchedText, self.lang, requiredActionsText, checkedActionsText)
	
	def strShort(self):
		out = self.matchedText
		if self.requiredActions:
			out = "({}) ".format(self.requiredActions[0]) + out
		return out
		
	def matchesText(self, text):
		return self.matchedText.lower() in text.lower()