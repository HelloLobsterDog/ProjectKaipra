from dirt.Water import Water

class GamePlayer(object):
	def __init__(self, viewpointCharacterID, lang = 'en-us'):
		self.water = Water(lang)
		self.viewpointCharacterID = viewpointCharacterID
		self.lang = lang
	
	def addWater(self, *water):
		for w in water:
			self.water.merge(w)
		
	@property
	def viewpointCharacter(self):
		char = self.water.lookupCharacter(self.viewpointCharacterID)
		if char == None:
			raise RuntimeError('viewpoint character ID was not found.')
		return char
	
	def displayNode(self):
		node = self.viewpointCharacter.currentNode
		text = node.formatTextBlock(self.lang)
		return text
	
	def handleInput(self, input):
		# build dict of template actions
		templateActions = {}
		templateActions.update(self.viewpointCharacter.currentNode.getTemplateActions())
		templateActions.update(self.viewpointCharacter.getTemplateActions())
		
		# build a list of available actions
		actions = []
		actions.extend(self.viewpointCharacter.currentNode.getActions())
		actions.extend(self.viewpointCharacter.actions)
		
		# see if any match
		output = []
		for action in actions:
			for trigger in action.getTriggers():
				if trigger.matches(input, templateActions, self.lang):
					preemption = trigger.preempt(templateActions, self.viewpointCharacter.currentNode, self.viewpointCharacter, self.lang)
					if preemption:
						# we have been preempted
						output.extend(preemption)
					else:
						# effects take place
						for effect in action.getEffects():
							out = effect.trigger(self.viewpointCharacter.currentNode, self.viewpointCharacter, self.lang)
							if out != None:
								output.append(out)
					return output
		
		if not output:
			# no action found
			output.append('that aint a command, chief.') # TODO
			return output
		