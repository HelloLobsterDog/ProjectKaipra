from ..xmlUtil import *
from ..ActionEffect import ActionEffect
from ..LangText import LangText

class ChangeNodeEffect(ActionEffect):
	def __init__(self, nodeID = None, printNode = True, xml = None):
		self.nodeID = nodeID
		self.printNode = printNode
		
		if xml != None:
			validateNoChildren(xml)
			validateAttributes(xml, ['type'], ['silent'])
			validateNoTail(xml)
			
			self.nodeID = xml.text
			if self.nodeID == None or self.nodeID.strip() == '':
				raise BadXMLError('node id is empty. What node will be changed to?')
			else:
				self.nodeID = self.nodeID.strip()
			
			if 'silent' in xml.attrib:
				silentText = xml.attrib[silent].strip().lower()
				if not silentText in ['true', 'false']:
					raise BadXMLError('value for silent is not the text "true" or "false", so it is invalid: ' + str(silentText))
				else:
					self.printNode = silentText == 'false'
			else:
				self.printNode = True
	
	def execute(self, character):
		character.changeNode(self.nodeID)
		if self.printNode:
			character.sendLangTextToController(character.getNodeLangText())
	