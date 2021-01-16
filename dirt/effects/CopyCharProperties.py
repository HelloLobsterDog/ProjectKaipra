from ..xmlUtil import *
from ..ActionEffect import ActionEffect
from ..LangText import LangText

class CopyCharProperties(ActionEffect):
	def __init__(self, copyFrom = None, copyTo = None, copyList = None, xml = None):
		self.copyFrom = None
		self.copyTo = None
		self.copyList = copyList
		
		if xml != None:
			validateNoChildren(xml)
			validateAttributes(xml, ['copyFrom'], ['copyTo'])
			validateNoTail(xml)
			
			self.copyFrom = xml.attrib['copyFrom']
			self.copyTo = xml.attrib.get('copyTo', None)
			
			if xml.text != None and xml.text.strip() != '':
				splitUp = [x.strip() for x in xml.text.strip().split(',')]
				self.copyList = []
				for thing in splitUp:
					if thing == 'currentNode':
						self.copyList.append('currentNodeID')
					elif thing == 'templateActions':
						self.copyList.append('templateActions')
					elif thing == 'state':
						self.copyList.append('state')
					elif thing == 'actions':
						self.copyList.append('actions')
					elif thing == 'species':
						self.copyList.append('speciesID')
					elif thing == 'skills':
						self.copyList.append('skills')
					else:
						raise BadXMLError('copy_char_properties does not recognize the property "' + thing + '"')
	
	def execute(self, character):
		water = character.water
		copiedInto = None
		if self.copyTo == None:
			copiedInto = character
		else:
			copiedInto = water.getCharacter(self.copyTo)
		
		copiedInto.copyFrom(water.getCharacter(self.copyFrom), self.copyList)
	