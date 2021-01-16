import logging

from .effects import BadCommandTextEffect
from .xmlUtil import *
from .util import parseBoolNoneSafe

class Character(object):
	def __init__(self, owningWater = None, xml = None, node = None):
		self.id = None
		self.currentNodeID = None
		self.controller = None
		self.templateActions = []
		self.state = {}
		self.actions = []
		self.speciesID = None
		self.skills = {}
		
		self.water = owningWater
		self.queuedEffects = []
		self.logger = logging.getLogger('dirt.character')
		
		if xml != None:
			self.logger.debug('handling character tag')
			validateNoTextOrTail(element)
			
			# attributes
			validateAttributes(element, ['id'], ['species', 'node'])
			self.id = element.attrib['id']
			self.speciesID = element.attrib.get('species', None)
			
			# children
			sortedChildren = sortChildren(xml, ['state_var', 'action', 'template_action', 'skill'])
			
			for stateVar in sortedChildren.get('state_var', []):
				self.logger.debug('handling state_var')
				validateNoChildren(stateVar)
				validateNoTextOrTail(stateVar)
				validateAttributes(stateVar, ['name', 'type', 'default'], [])
				self.state[stateVar.attrib['name']] = parseState(stateVar.attrib['name'], stateVar.attrib['type'], stateVar, self.logger)
			
			for action in sortedChildren.get('action', []):
				self.logger.debug('handling action tag')
				self.addAction(Action(action, self.water.defaultLang))
			
			for templateAction in sortedChildren.get('template_action', []):
				self.logger.debug('handling template action tag')
				self.addTemplateAction(TemplateAction(xml = templateAction, defaultLang = self.water.defaultLang))
				
			for knownSkill in sortedChildren.get('skill', []):
				self.logger.debug('handling known skill tag')
				validateNoChildren(knownSkill)
				validateNoTextOrTail(knownSkill)
				validateAttributes(knownSkill, ['id', 'skill'], ['ignore_prerequisites'])
				self.learnSkill(knownSkill.attrib['id'], knownSkill.attrib['skill'], parseBoolNoneSafe(knownSkill.attrib.get('ignore_prerequisites', None), False))
			
			# node
			xmlNode = element.attrib.get('node', None)
			if xmlNode != None:
				# provided in xml, so it needs to not be in the constructor
				if node != None:
					raise BadXMLError('character is defined in a node, but it declares a node in its tag. You can only do one or the other.')
				else:
					self.currentNodeID = xmlNode
			else:
				# not provided in xml
				self.currentNodeID = node
				if node == None:
					raise ValueError('Node not provided. Characters must have nodes.')
	
	def copyFrom(self, target, copyList):
		if copyList == None:
			copyList = ['currentNodeID', 'templateActions', 'state', 'actions', 'speciesID', 'skills']
		for thing in copyList:
			setattr(this, thing, getattr(target, thing))
	
	
	
	@property
	def hasSpecies(self):
		return self.speciesID != None
	
	@property
	def species(self):
		return self.water.getSpecies(self.speciesID)
		
		
		
	def getNodeLangText(self):
		return self.water.getNode(self.currentNodeID).textBlock
	
	def performCommandText(self, text, lang):
		if self.water == None:
			raise RuntimeError("character is disconnected from a water instance, so actions cannot be performed")
			
		self.logger.info('Character id "%s" is attempting to perform action text "%s" with lang %s', self.id, text, lang)
		
		# logging for all available actions.
		if self.logger.isEnabledFor(logging.DEBUG):
			self.logger.debug('All possible actions: [%s]', ", ".join([str(x) for x in self.getAllAvailableActions()]))
		
		# see if we match any of our available actions
		for action in self.getAllAvailableActions():
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
		for key, val in self.state.items():
			state['char.' + key] = val
		return state
	
	def getWriteDict(self):
		# note to self: changes/additions to this method need to be mirrored in getStateDict
		out = dict()
		out['node'] = self.getNode().state
		out['char'] = self.state
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
	
	def getAllAvailableActions(self):
		'''
		Returns a generator which iterates over all the actions available to the character.
		'''
		yield from self.getNode().actions
		yield from self.actions
		if self.hasSpecies:
			yield from self.species.actions
	
	def getTemplateAction(self, id, fromEverywhere = True):
		'''
		Looks up a template action that is available to us given it's ID.
		If not found, returns None.
		If fromEverywhere is True, it will look everywhere that is available to us, if false, it will only look in the character's template actions, and our species template actions.
		'''
		# node
		if fromEverywhere:
			fromNode = self.getNode().getTemplateAction(id)
			if fromNode != None:
				return fromNode
		# from us
		for action in self.templateActions:
			if action.id == id:
				return action
		# from species
		if self.hasSpecies:
			for action in self.species.templateActions:
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
		
	def addAction(self, action):
		self.actions.append(action)
		
	def learnSkill(self, treeID, skillID, ignorePrerequisites = False):
		treeList = self.skills.setdefault(treeID, [])
		# remove if we already have it
		for index, skill in enumerate(treeList):
			if skill[0] == skillID:
				del treeList[index]
		# add
		treeList.append((skillID, ignorePrerequisites))
		
	def hasSkill(self, treeID, skillID):
		treeList = self.skills.get(treeID, [])
		for skill in treeList:
			if skill[0] == skillID:
				return True
		return False
	
	def skillIgnoresPrerequisites(self, treeID, skillID, defaultIfSkillNotKnown = None):
		treeList = self.skills.get(treeID, [])
		for skill in treeList:
			if skill[0] == skillID:
				return skill[1]
		return defaultIfSkillNotKnown
	