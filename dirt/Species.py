import logging

from .xmlUtil import *

class Species(object):
	def __init__(self, xml = None, owningWater = None, ):
		self.id = None
		self.templateActions = []
		self.actions = []
		
		self.water = owningWater
		self.logger = logging.getLogger('dirt.species')
		
		if xml != None:
			self.logger.debug('handling species tag')
			validateNoTextOrTail(element)
			
			# attributes
			validateAttributes(element, ['id'], [])
			self.id = element.attrib['id']
			
			# children
			sortedChildren = sortChildren(xml, ['action', 'template_action'])
			
			for action in sortedChildren.get('action', []):
				self.logger.debug('handling action tag')
				self.addAction(Action(action, self.water.defaultLang))
			
			for templateAction in sortedChildren.get('template_action', []):
				self.logger.debug('handling template action tag')
				self.addTemplateAction(TemplateAction(xml = templateAction, defaultLang = self.water.defaultLang))
	
	# not a whole lot in here right now. Everything uses it's attributes directly...