from ..xmlUtil import *
from ..ActionEffect import ActionEffect
from ..LangText import LangText

class DisplayTextEffect(ActionEffect):
	def __init__(self, text = None, lang = None, xml = None):
		self.text = text
		self.lang = lang
		
		if xml != None:
			# this effect has type and lang in the attributes, and text in the body
			validateNoChildren(xml)
			validateAttributes(xml, ['type'], ['lang'])
			validateNoTail(xml)
			
			self.text = xml.text
			if self.text == None or self.text.strip() == '':
				raise BadXMLError('text is empty. What will be displayed to the player?')
			else:
				self.text = self.text.strip()
			if 'lang' in xml.attrib:
				self.lang = xml.attrib['lang'].strip()
	
	def execute(self, character):
		lt = LangText()
		lang = self.lang
		if lang == None:
			lang = character.water.defaultLang
		lt.add(lang, self.text)
		character.sendLangTextToController(lt)
	