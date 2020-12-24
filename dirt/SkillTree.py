import logging

from .xmlUtil import *
from .Skill import Skill

class SkillTree(object):
	def __init__(self, element = None, defaultLang = None):
		self.skills = dict()
		self.id = None
		
		self.defaultLang = defaultLang
		
		self.logger = logging.getLogger('dirt.SkillTree')
		
		if element != None:
			self.logger.debug('handling skill_tree tag')
			validateNoTextOrTail(element)
			validateAttributes(element, ['id'], [])
			
			self.id = element.attrib['id']
			
			for child in element:
				if child.tag != 'skill':
					raise BadXMLError('skill_tree tag only allows skill tags. Found: ' + child.tag)
				self.addSkill(Skill(child, self.defaultLang))
	
	def addSkill(self, skill):
		self.skills[skill.id] = skill