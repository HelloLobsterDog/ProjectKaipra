import logging

from .xmlUtil import *
from .util import parseMatchTypes

class ActionCondition(object):
	def __init__(self, var = None, equalTo = None, xml = None):
		self.var = var
		self.equalTo = equalTo
		
		self.logger = logging.getLogger('dirt.actioncondition')
		
		if xml != None:
			self.logger.debug('handling condition tag')
			validateNoChildren(xml)
			validateAttributes(xml, ['var'], [])
			validateNoTail(xml)
			
			if 'var' in xml.attrib:
				self.var = xml.attrib['var'].strip()
			else:
				raise BadXMLError('Condition tag is missing var attribute. What variable will be read by the condition?')
			
			if xml.text != None and xml.text.strip() != '':
				self.equalTo = xml.text.strip()
			else:
				raise BadXMLError('Condition tag is missing text, or it is empty. What is the expected value?')
	
	def __str__(self):
		return 'ActionCondition<var="{}" equalTo="{}">'.format(self.var, self.equalTo)
	
	def isMet(self, character):
		state = character.getStateDict()
		if not self.var in state:
			raise RuntimeError('Variable name "{}" does not exist to read.')
		else:
			valueInState = state[self.var]
			# determine the type to parse based on the type of the value in the state dict and parse our string to that type
			self.logger.debug('Parsing value "%s" into type %s based on existing value "%s"', self.equalTo, valueInState.__class__, valueInState)
			parsedEqualTo = parseMatchTypes(self.equalTo, valueInState)
			# finally, compare the two
			self.logger.debug('comparing values "%s" and "%s" (current value in state, desired value)', valueInState, parsedEqualTo)
			return valueInState == parsedEqualTo
	