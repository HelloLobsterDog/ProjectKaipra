import logging

from .xmlUtil import *
from .ActionTrigger import ActionTrigger
from .ActionCondition import ActionCondition
from .effects import effectFactory

class Action(object):
	def __init__(self, element = None, defaultLang = None):
		self.triggers = []
		self.conditions = []
		self.effects = []
		
		self.defaultLang = defaultLang
		self.logger = logging.getLogger('dirt.action')
		
		if element != None:
			self.logger.debug('handling action tag')
			validateNoTextOrTail(element)
			validateNoAttributes(element)
			actionChildren = sortChildren(element, ['trigger', 'effect', 'condition'])
			
			for trigger in actionChildren.get('trigger', []):
				validateNoTail(trigger)
				validateNoChildren(trigger)
				validateAttributes(trigger, [], ['uses', 'target_for', 'lang'])
				
				contents = trigger.text
				if contents == None:
					raise BadXMLError('Trigger tag has no text. What triggers it?')
				contents = contents.strip()
				lang = trigger.attrib.get('lang', self.defaultLang)
				if lang != None:
					lang = lang.strip()
				else:
					lang = self.defaultLang
				checkedActions = []
				requiredActions = []
				if 'uses' in trigger.attrib:
					checkedActions.append(trigger.attrib['uses'].strip())
				if 'target_for' in trigger.attrib:
					val = trigger.attrib['target_for'].strip()
					requiredActions.append(val)
					checkedActions.append(val)
				# have everything we need. Put together trigger and return it.
				self.addTrigger(ActionTrigger(contents, requiredActions, checkedActions, lang))
				
			for effect in actionChildren.get('effect', []):
				self.addEffect(effectFactory(effect, self.defaultLang))
			
			for condition in actionChildren.get('condition', []):
				self.addCondition(ActionCondition(xml = condition))
	
	def __str__(self):
		first = None
		if self.triggers:
			first = self.triggers[0].strShort()
		return 'Action<trigger 1 of {}: "{}". {} effects>'.format(len(self.triggers), first, len(self.effects))
	
	def addTrigger(self, trigger):
		self.triggers.append(trigger)
	
	def addCondition(self, condition):
		self.conditions.append(condition)
	
	def addEffect(self, effect):
		self.effects.append(effect)
		
	def matches(self, text, lang, character):
		for index, trigger in enumerate(self.triggers):
			triggerLang = trigger.lang
			if triggerLang == None:
				triggerLang = self.defaultLang
			# quick and easy checks for whether the language is the same and if the text matches
			if triggerLang == lang and trigger.matchesText(text):
				# check template actions
				allMatch = True
				for requiredName in trigger.requiredActions:
					requiredActual = character.getTemplateAction(requiredName)
					if requiredActual == None:
						raise RuntimeError('character id "{}" could not look up template action "{}"'.format(character.id, requiredName))
					if not requiredActual.matches(text, lang):
						allMatch = False
						character.logger.debug('text for action trigger #%d matches the trigger, but does not match required template action "%s"', index + 1, requiredName)
				if allMatch:
					character.logger.info('Text and template actions for action trigger #%d matches: %s', index + 1, trigger)
					return True
			else:
				character.logger.debug('text for action trigger #%d does not match.', index + 1)
		return False
	