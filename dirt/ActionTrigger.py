

class ActionTrigger(object):
	def __init__(self, matchedText, requiredTemplateActions = None, checkedTemplateActions = None, lang = 'en-us'):
		self.matchedText = matchedText
		self.lang = lang
		
		self.checkedTemplateActions = []
		if checkedTemplateActions != None:
			self.checkedTemplateActions.extend(checkedTemplateActions)
		self.requiredTemplateActions = []
		if requiredTemplateActions != None:
			self.requiredTemplateActions.extend(requiredTemplateActions)
			self.checkedTemplateActions.extend(requiredTemplateActions)
	
	def matches(self, inputText, templateActions, lang = 'en-us'):
		if lang == self.lang:
			# matched text in the input text?
			if self.matchedText.lower() in inputText.lower():
				# required templates in the text?
				allMatch = True
				for reqTemplate in self.requiredTemplateActions:
					realTemplate = templateActions.get(reqTemplate, None)
					if realTemplate != None:
						if not realTemplate.matches(inputText, lang):
							allMatch = False
							break
					else:
						raise ValueError('required template action name "{}" not found in actual template actions list'.format(reqTemplate))
				if allMatch:
					return True # we match the text ourselves, and the required template actions are matching
				else:
					return False # we match, but our required template actions do not
			else:
				return False # our matched text isn't in the input
		else:
			return False # wrong lang
	
	def preempt(self, templateActions, node, viewpointCharacter, lang = 'en-us'):
		'''
		This method gives the template actions an opportunity to preempt the action effect.
		This is used for cases where the player does something like use the look command, but they are blind.
		This means this is a valid action, and would have worked, but the template action "preempts" it, such that
		the action effects do not take place, and the template action does something instead (this is usually going
		to be just printing some text).
		
		This method assumes that the matches() method has returned True. It returns a list of text to show to the user.
		If empty, no preemption takes place, but if not empty, preemption takes place.
		'''
		preemption = []
		for template in self.checkedTemplateActions:
			realTemplate = templateActions.get(template, None)
			if realTemplate != None:
				preemptText = realTemplate.preempt(node, viewpointCharacter, lang)
				if preemptText != None:
					preemption.append(preemptText)
			else:
				raise ValueError('Checked template action name "{}" not found in actual template actions list'.format(template))
		return preemption