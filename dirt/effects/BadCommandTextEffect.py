from ..xmlUtil import *
from ..ActionEffect import ActionEffect

class BadCommandTextEffect(ActionEffect):
	def __init__(self, xml = None):
		if xml != None:
			# this effect has nothing but type in the tag, and no body or children.
			validateNoChildren(xml)
			validateAttributes(xml, ['type'], [])
			validateNoTextOrTail(xml)
	
	def execute(self, character):
		character.sendLangTextToController(character.water.badCommandText)
	