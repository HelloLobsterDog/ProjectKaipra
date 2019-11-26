from dirt.Check import Check, BadReadFromNameError, BadLangError
from collections import namedtuple

class ChoiceCheck(Check):
	Storage = namedtuple('ChoiceCheckStorage', ['acceptableValues', 'langTexts'])
	OutputType = namedtuple('ChoiceCheckOutputType', ['text', 'lang', 'formatted'])
	
	def __init__(self, name, readFrom):
		super().__init__(name, readFrom)
		self.outputs = []
		
	def addTextForValues(self, acceptableVals, text, lang = 'en-us', formatted = False):
		'''
		Given the values which will be accepted, this method adds the text for the lang provided as output.
		'''
		# do we already have the values this will go into?
		toAdd = None
		for existing in self.outputs:
			if existing.acceptableValues == acceptableVals:
				toAdd = existing.langTexts
		# if not found, add the values, so we can put the text into it
		if toAdd == None:
			x = ChoiceCheck.Storage(acceptableValues = acceptableVals, langTexts = [])
			self.outputs.append(x)
			toAdd = x.langTexts
		# put the text into it
		toAdd.append(ChoiceCheck.OutputType(text, lang, formatted))
	
	def get(self, stateDict, lang, defaultLang):
		'''
		This method checks the value of the state dict, and returns the value configured,
		along with whether or not it has nested checks. If the lang is not present, the defaultLang
		will be used, and if that is not present, an exception should be raised.
		'''
		state = stateDict.get(self.readFrom, None)
		if state == None:
			raise BadReadFromNameError('readFrom name "{}" not present in the state dict.'.format(self.readFrom))
		
		for possible in self.outputs:
			for accepted in possible.acceptableValues:
				# match?
				acceptable = False
				if accepted == None: # acceptable values which include None will accept anything (sortof like including an else statement)
					acceptable = True
				else:
					val = accepted
					# parse the value to the correct type to be sure they will compare
					callable = None
					if isinstance(state, int):
						callable = int
					elif isinstance(state, float):
						callable = float
					if callable != None:
						val = callable(val)
					acceptable = state == val
				
				# if acceptable, find the language
				if acceptable:
					langTexts = possible.langTexts
					# found it. Need to find the lang in there.
					for out in langTexts:
						if out.lang == lang:
							return out.text, out.formatted
					# if we're down here, we probably need to fall back to the default lang
					for out in langTexts:
						if out.lang == defaultLang:
							return out.text, out.formatted
					# if we're down here, we didn't find anything
					raise BadLangError('lang "{}" and default lang "{}" does not have text.'.format(lang, defaultLang))
		
		# if we're down here, we never found anything
		raise RuntimeError('could not find a value which matches the choice check reading from "{}"'.format(self.readFrom))