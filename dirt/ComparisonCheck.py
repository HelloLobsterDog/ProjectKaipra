from dirt.Check import Check, BadReadFromNameError, BadLangError
from collections import namedtuple

class ComparisonCheck(Check):
	LESS_THAN = 0
	LESS_THAN_OR_EQUAL = 1
	EQUAL = 2
	GREATER_THAN_OR_EQUAL = 3
	GREATER_THAN = 4
	
	Storage = namedtuple('ComparisonCheckStorage', ['comparisons', 'langTexts'])
	Comparison = namedtuple('ComparisonCheckComparison', ['type', 'value'])
	OutputType = namedtuple('ComparisonCheckOutputType', ['text', 'lang', 'formatted'])
	
	def __init__(self, name, readFrom):
		super().__init__(name, readFrom)
		self.outputs = [] # list of ComparisonCheck.Storage
		
	def addOutput(self, comparisons, text, lang = 'en-us', formatted = False):
		# do we already have the comparisons this will go into?
		toAdd = None
		for existing in self.outputs:
			if existing.comparisons == comparisons:
				toAdd = existing.langTexts
		# if not found, add the comparisons, so we can put the text into it
		if toAdd == None:
			x = ComparisonCheck.Storage(comparisons = comparisons, langTexts = [])
			self.outputs.append(x)
			toAdd = x.langTexts
		# put the text into it
		toAdd.append(ComparisonCheck.OutputType(text, lang, formatted))
		
	
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
			# check if all the comparisons match
			allMatch = True
			for comparison in possible.comparisons:
				if comparison.type == ComparisonCheck.LESS_THAN:
					if not (state < comparison.value):
						allMatch = False
						break
				elif comparison.type == ComparisonCheck.LESS_THAN_OR_EQUAL:
					if not (state <= comparison.value):
						allMatch = False
						break
				elif comparison.type == ComparisonCheck.EQUAL:
					if not (state == comparison.value):
						allMatch = False
						break
				elif comparison.type == ComparisonCheck.GREATER_THAN_OR_EQUAL:
					if not (state >= comparison.value):
						allMatch = False
						break
				elif comparison.type == ComparisonCheck.GREATER_THAN:
					if not (state > comparison.value):
						allMatch = False
						break
				else:
					raise RuntimeError('comparison type "{}" is not recognized'.format(comparison.type))
					
			if allMatch:
				# yes, they all match, so now we need to find our output in the langs
				langTexts = possible.langTexts
				# check lang first
				for text in langTexts:
					if text.lang == lang:
						return text.text, text.formatted
				# check defaultLang next
				for text in langTexts:
					if text.lang == defaultLang:
						return text.text, text.formatted
				# if we're here, we don't have the lang or default lang
				raise BadLangError('lang "{}" and default lang "{}" does not have text.'.format(lang, defaultLang))
				
		# if we're down here, we never found anything
		raise RuntimeError('could not find a value which matches the comparison check.')
		