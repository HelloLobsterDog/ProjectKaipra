from .xmlUtil import *
from .LangText import LangText

class TemplateAction(object):
	
	def __init__(self, id = None, xml = None, defaultLang = None):
		self.id = id
		self.defaultLang = defaultLang
		self.matchedText = []
		
		if xml != None:
			validateNoTextOrTail(xml)
			validateAttributes(xml, ['id'], [])
			
			self.id = xml.attrib['id']
			if self.id == None or self.id.strip() == "":
				raise RuntimeError('template action id is empty')
			else:
				self.id = self.id.strip()
			
			sortedChildren = sortChildren(xml, ['matched_text'])
			for text in sortedChildren.get('matched_text', []):
				validateNoTail(text)
				validateAttributes(text, [], ['lang'])
				# lang
				lang = text.attrib.get('lang', self.defaultLang)
				if lang == None or lang.strip() == '':
					lang = self.defaultLang
				# text
				t = text.text
				if text == None or t.strip() == '':
					raise RuntimeError('text of matched_text cannot be empty. What text is matched?')
				# actual langtext
				lt = LangText()
				lt.add(lang, t.strip())
				self.matchedText.append(lt)
	
	def getFirstMatchedText(self):
		if not self.matchedText:
			return None
		return self.matchedText[0].getFirst()[1]
	
	def matches(self, text, lang):
		for matched in self.matchedText:
			forLang = matched.get(lang, self.defaultLang)
			if forLang != None:
				if forLang.lower() in text.lower():
					return True
		return False
	