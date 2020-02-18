from ..xmlUtil import *
from ..util import parseMatchTypes
from ..ActionEffect import ActionEffect

class SetVarEffect(ActionEffect):
	def __init__(self, var = None, value = True, xml = None):
		self.var = var
		self.value = value
		
		if xml != None:
			validateNoChildren(xml)
			validateAttributes(xml, ['type', 'var'], [])
			validateNoTail(xml)
			
			if xml.text != None and xml.text.strip() != '':
				self.value = xml.text.strip()
			else:
				raise BadXMLError('set_var effect has no text. What will the var be set to?')
			
			self.var = xml.attrib['var'].strip()
			if self.var == '':
				raise BadXMLError('set_var var attribute is empty.')
	
	def execute(self, character):
		# read existing value to get the type of the variable
		state = character.getStateDict()
		if not self.var in state:
			raise RuntimeError('Variable name "{}" does not exist.'.format(self.var))
		# get value in the correct type
		parsedValue = parseMatchTypes(self.value, state[self.var])
		# get dict to write into and where to write it
		split = self.var.split('.', maxsplit = 1)
		if len(split) != 2:
			raise RuntimeError('variable name "{}" does not contain a . to differentiate where the variable comes from'.format(self.var))
		writeDictName = split[0]
		writeDictValueName = split[1]
		# retrieve the dict
		writeDict = character.getWriteDict().get(writeDictName, None)
		if writeDict == None:
			raise RuntimeError('location to write to, "{}", does not exist. Trying to write name "{}" there.'.format(writeDictName, writeDictValueName))
		# write
		writeDict[writeDictValueName] = parsedValue
	