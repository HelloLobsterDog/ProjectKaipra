

class LangText(object):
	'''
	Wrapper around a dictionary, providing different versions of the same text in different languages.
	'''
	def __init__(self, lang = None, text = None):
		if lang != None and text != None:
			self.texts = {lang : text}
		else:
			self.texts = {}
	
	def getFirst(self):
		for lang in self.texts:
			return (lang, self.texts[lang])
	
	def get(self, lang, defaultLang = None):
		if lang in self.texts:
			return self.texts[lang]
		elif defaultLang in self.texts:
			return self.texts[defaultLang]
		else:
			return None
	
	def hasText(self, lang, defaultLang = None):
		return lang in self.texts or (defaultLang != None and defaultLang in self.texts)
	
	def add(self, lang, text):
		self.texts[lang] = text
	
	def remove(self, lang):
		del self.texts[lang]
		
	def merge(self, other, overwriteExisting = False):
		for key, value in other.texts.items():
			if not key in self.texts or overwriteExisting:
				self.texts[key] = value
	