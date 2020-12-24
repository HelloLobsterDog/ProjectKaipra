import logging

from .xmlUtil import *
from .LangText import LangText

class Skill(object):
	def __init__(self, element = None, defaultLang = None):
		self.text = LangText()
		self.names = LangText()
		self.id = None
		self.prerequisites = []
		
		self.defaultLang = defaultLang
		
		self.logger = logging.getLogger('dirt.Skill')
		
		if element != None:
			self.logger.debug('handling skill tag')
			validateNoTextOrTail(element)
			validateAttributes(element, ['id'], [])
			children = sortChildren(element, ['text', 'prerequisite'])
			
			self.id = element.attrib['id']
			
			if not 'text' in children:
				raise BadXMLError('one or more text tags are required to be present in a skills.')
			for child in children.get('text', []):
				validateAttributes(child, ['name'], ['lang'])
				validateNoTail(child)
				validateNoChildren(child)
				validateHasText(child)
				lang = child.attrib.get('lang', self.defaultLang)
				self.names.add(lang, child.attrib['name'])
				self.text.add(lang, child.text)
			
			for child in children.get('prerequisite', []):
				validateNoTextOrTail(child)
				validateNoChildren(child)
				validateAttributes(child, ['id', 'weight'], [])
				self.prerequisites.append((child.attrib['id'], child.attrib['weight']))