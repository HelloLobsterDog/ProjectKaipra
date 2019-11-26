

class Node(object):

	def __init__(self, id):
		self.id = id
		
		# dictionary of {lang id string : text block}. Until validate has been called, we don't know if check names are valid, or if the lang string ids are real language identifiers.
		self.text = {}
		
		# List of Check subclass instances. Until validate has been called, we don't know if they are valid individually, if the names are unique,
		# if the based_on value exists, or if all the checks called for in the text blocks are present in the list.
		self.checks = []
		
		# List of actions.
		self.actions = []
		# template actions (like go, look, etc, but specific to the node)
		self.templateActions = {}
		
		# Dictionary of {var name string : value (any type)}
		self.state = {}
		
		# List of strings containing validation problems. If the list has anything in it, it's not valid.
		# Storing this on the node allows us to build up a list and present the user with as many problems as we can, all at once, as opposed to blowing up the first time we find something wrong,
		# forcing them to fix that one thing and try again, only to find another thing, and another, and another, repeat ad nauseum, each time making one edit and running the program again.
		# That may be easier to program, which would mean we wouldn't do this, but it's not easy to work with, it's painful and annoying. (I'm looking at you, compiler authors)
		self.problems = []
		
		
	#####################################################################
	# the basic add/get/etc methods, mostly used while creating the node:
	def addText(self, text, lang):
		'''
		Adds the text block to the node for the language passed.
		If the node already has a text block for the language, it will be overwritten.
		'''
		self.text[lang] = text
	
	def hasText(self, lang):
		''' Returns whether or not the language passed has a text block '''
		return lang in self.text
	
	def getText(self, lang, defaultLang = 'en-us'):
		'''
		Gets the text of the node in the language passed.
		If that language does not have a text, the text from the defaultLang is returned.
		If that language also does not exist, an exception will be thrown.
		'''
		if lang in self.text:
			return self.text[lang]
		else:
			return self.text[defaultLang]
		
	
	def addCheck(self, check):
		''' Adds the check passed to the list of checks. Does not ensure it's validity. '''
		self.checks.append(check)
	
	def hasCheck(self, name):
		''' Returns whether or not a check has the name provided. '''
		for check in self.checks:
			if check.name == name:
				return True
		return False
	
	def getCheck(self, name):
		''' Returns a Check instance with the name passed, or None if no such check exists. '''
		for check in self.checks:
			if check.name == name:
				return check
		return None
		
		
	def addAction(self, action):
		''' This method is equivalent to writing "node.actions.append(action)" but it's nicer to read. '''
		self.actions.append(action)
	
	def getActions(self):
		return self.actions
		
		
	def getTemplateActions(self):
		return self.templateActions
	
	
	#####################################################################
	# The complex important stuff, called mostly by gameplay code:
	def formatTextBlock(self, lang, defaultLang = 'en-us'):
		return self.formatText(self.getText(lang, defaultLang), lang, defaultLang)
		
	def formatText(self, text, lang, defaultLang = 'en-us'):
		'''
		Formats the text of the node for the language passed, filling in the text block with the output of the node's checks.
		'''
		# put together state dict from which checks will read
		allState = dict()
		for key, val in self.state.items():
			allState['node.' + key] = val
		
		# put together the formatting dict using checks
		fmt = dict()
		needAnotherPass = list()
		for check in self.checks:
			result, formatted = check.get(allState, lang, defaultLang)
			fmt[check.name] = result
			if formatted:
				needAnotherPass.append(check.name)
		
		# Format dict is complete now. We can now format the parts of the dict that require double formatting
		for name in needAnotherPass:
			fmt[name] = fmt[name].format(**fmt)
		
		# format the text block
		return text.format(**fmt)
	
	def getAction(self, input, character):
		'''
		Given the input from the user, this method returns an action that would be triggered by this input,
		or None if no action is valid for the input. The character passed is the viewpoint character which
		will be carrying out the action.
		'''
		return None
	
	def validate(self, character):
		'''
		This method validates the Node, returning a list of strings describing problems with the Node, to
		be shown to the user. If the list is empty, the Node lacks problems, and is "valid".
		'''
		problems = []
		return problems
	