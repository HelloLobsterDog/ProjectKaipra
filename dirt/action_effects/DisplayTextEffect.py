from dirt.ActionEffect import ActionEffect

class DisplayTextEffect(ActionEffect):
	def __init__(self, text, lang, formatted = False):
		self.text = text
		self.lang = lang
		self.formatted = formatted
	
	def trigger(self, node, viewpointCharacter, lang = 'en-us'):
		if lang == self.lang:
			# TODO: format our text if formatting
			return self.text
		return None