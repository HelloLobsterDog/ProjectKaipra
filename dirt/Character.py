import logging

from .effects import BadCommandTextEffect

class Character(object):
	def __init__(self, owningWater = None):
		self.id = None
		self.currentNodeID = None
		self.controller = None
		self.templateActions = []
		
		self.water = owningWater
		self.queuedEffects = []
		self.logger = logging.getLogger('dirt.character')
		
	def getNodeLangText(self):
		return self.water.getNode(self.currentNodeID).textBlock
	
	def performCommandText(self, text, lang):
		if self.water == None:
			raise RuntimeError("character is disconnected from a water instance, so actions cannot be performed")
			
		self.logger.info('Character id "%s" is attempting to perform action text "%s" with lang %s', self.id, text, lang)
		
		# compile a list of actions that can be performed
		possible = []
		possible.extend(self.getNode().actions)
		self.logger.debug('All possible actions: [%s]', ", ".join([str(x) for x in possible]))
		
		# see if we match any of them
		for action in possible:
			self.logger.debug('checking if action matches: ' + str(action))
			if action.matches(text, lang, self):
				# check conditions
				conditionsMatch = True
				for index, cond in enumerate(action.conditions):
					if not cond.isMet(self):
						self.logger.info('Action matches, but condition #%s of %d does not: %s', index + 1, len(action.conditions), cond)
						conditionsMatch = False
						break
				if conditionsMatch:
					self.logger.info('Action matches and %d conditions are met.', len(action.conditions)) # conditions pass
					# perform the action
					self.logger.info('Action is running. %d effects being enqueued.', len(action.effects))
					for effect in action.effects:
						self.enqueueEffect(effect)
					return
		# if we're down here we didn't find any actions
		self.logger.info('No action found for the command text.')
		self.enqueueEffect(BadCommandTextEffect())
		
	def formatText(self, unformatted, lang):
		# assemble state dict
		allState = self.getStateDict()
		
		# assemble formatting dict via getting text out of checks with state dict
		fmt = dict()
		for check in self.getNode().checks:
			checkLangText = check.getText(allState)
			if checkLangText == None:
				raise RuntimeError('Check "{}" did not return text.')
			fmt[check.name] = checkLangText.get(lang, self.water.defaultLang)
		
		# format until the text lacks braces or nothing changes
		toFormat = unformatted.format(**fmt)
		previous = toFormat
		while '{' in toFormat: # this may get more complicated if we ever want curly braces to show up in actual text
			toFormat = unformatted.format(**fmt)
			if toFormat == previous:
				break # did not change
			previous = toFormat
		return toFormat
		
	def getStateDict(self):
		# note to self: changes/additions to this method need to be mirrored in getWriteDict
		state = dict()
		for key, val in self.getNode().state.items():
			state['node.' + key] = val
		return state
	
	def getWriteDict(self):
		# note to self: changes/additions to this method need to be mirrored in getStateDict
		out = dict()
		out['node'] = self.getNode().state
		return out
		
	def enqueueEffect(self, effect):
		self.queuedEffects.append(effect)
		self.water.markCharacterHasActions(self)
	
	def executeEffects(self):
		while self.queuedEffects:
			effect = self.queuedEffects.pop(0)
			self.logger.info('Character id "%s" performing action effect: %s', self.id, effect)
			effect.execute(self)
	
	def hasQueuedEffects(self):
		return self.queuedEffects
	
	def sendLangTextToController(self, langText):
		'''
		Sends whatever langtext is passed to the controller of this character.
		If the character is not controlled by anyone, this method doesn't do anything.
		'''
		if self.controller != None: # the only thing this stores for the moment is the userID, so non-none means controlled by a player
			self.water.server.send(self.controller, langText)
			
	def addTemplateAction(self, action):
		# check for duplicates
		for templateAction in self.templateActions:
			if templateAction.id == action.id:
				raise RuntimeError("template action ID " + templateAction.id + " is duplicated")
		# add
		self.templateActions.append(action)
	
	def getTemplateAction(self, id, fromEverywhere = True):
		# node
		if fromEverywhere:
			fromNode = self.getNode().getTemplateAction(id)
			if fromNode != None:
				return fromNode
		# from us
		for action in self.templateActions:
			if action.id == id:
				return action
		# from Water
		if fromEverywhere:
			fromWater = self.water.getTemplateAction(id)
			if fromWater != None:
				return fromWater
		return None
		
	def getNode(self):
		return self.water.getNode(self.currentNodeID)
	
	def changeNode(self, nodeID):
		if self.water.getNode(nodeID) == None:
			raise RuntimeError('node ID "' + nodeID + '" does not exist.')
		self.currentNodeID = nodeID
	