

class TemplateAction(object):
	def __init__(self, id, langTexts, defaultLang = 'en-us'):
		self.id = id # string (like "go")
		self.langTexts = langTexts # dict {lang: list [text which matches]}
		self.defaultLang = defaultLang
	
	def matches(self, inputText, lang):
		# get the configured text for the lang
		matchesForLang = self.langTexts.get(lang, None)
		if matchesForLang == None: # try the default lang
			matchesForLang = self.langTexts.get(self.defaultLang, None)
		if matchesForLang == None: # didn't find the lang OR the default lang
			raise ValueError('template action with id "{}" cannot find text with lang "{}" or its default lang "{}"'.format(self.id, lang, self.defaultLang))
		# we've got the configured text for the lang
		for text in matchesForLang:
			if text in inputText:
				return True
		return False
		
	def preempt(self, node, viewpointCharacter, lang):
		'''
		Allows the template action to preempt an action trigger, which would otherwise trigger because our text matches,
		but which cannot occur because the template action decides it can't. This is used in cases where, as an example,
		you attempt to look at something, but your character is blind - it's a valid thing to do, but the action's effects
		can't be allowed to complete by the template action stopping it.
		
		Returns a string of text to show to the user if preempting, or None if not preempting.
		'''
		raise NotImplementedError('subclasses must override this method and implement it.')
