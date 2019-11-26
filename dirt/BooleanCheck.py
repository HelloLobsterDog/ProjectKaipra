from dirt.Check import Check, BadReadFromNameError, BadLangError
from collections import namedtuple

class BooleanCheck(Check):
	OutputType = namedtuple('BooleanCheckOutputType', ['text', 'lang', 'formatted'])
	
	def __init__(self, name, readFrom):
		super().__init__(name, readFrom)
		self.true = []
		self.false = []
		
	def addOutput(self, boolValue, text, lang = 'en-us', formatted = False):
		out = None
		if boolValue:
			out = self.true
		else:
			out = self.false
		out.append(BooleanCheck.OutputType(text, lang, formatted))
	
	def get(self, stateDict, lang, defaultLang):
		'''
		This method checks the value of the state dict, and returns the value configured,
		along with whether or not it has nested checks. If the lang is not present, the defaultLang
		will be used, and if that is not present, an exception should be raised.
		'''
		state = stateDict.get(self.readFrom, None)
		if state == None:
			raise BadReadFromNameError('readFrom name "{}" not present in the state dict.'.format(self.readFrom))
		
		out = None
		if state:
			out = self.true
		else:
			out = self.false
		
		# try it with lang
		for text in out:
			if text.lang == lang:
				return text.text, text.formatted
		# if we're down here we didn't find it, so use the default lang
		for text in out:
			if text.lang == defaultLang:
				return text.text, text.formatted
		# if we're down here, we didn't find it at all.
		raise BadLangError('lang "{}" and default lang "{}" does not have text.'.format(lang, defaultLang))
		