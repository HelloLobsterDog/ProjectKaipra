from ..xmlUtil import *
from ..ActionEffect import ActionEffect
from ..LangText import LangText

class DisplayNodeTextEffect(ActionEffect):
	def __init__(self, xml = None):
		if xml != None:
			# this effect has type in the attributes, and nothing else.
			validateNoChildren(xml)
			validateAttributes(xml, ['type'], [])
			validateNoTail(xml)
			validateNoBody(xml)
	
	def execute(self, character):
		character.sendLangTextToController(character.getNodeLangText())
	