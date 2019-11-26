

class BadReadFromNameError(RuntimeError):
	pass

class BadLangError(RuntimeError):
	pass

class Check(object):
	'''
	Base class of all Checks, and it presents the basic interface that is required of them.
	'''
	
	def __init__(self, name, readFrom):
		self.name = name
		self.readFrom = readFrom
	
	def get(self, stateDict, lang, defaultLang):
		'''
		This method checks the value of the state dict, and returns the value configured,
		along with whether or not it has nested checks. If the lang is not present, the defaultLang
		will be used, and if that is not present, an exception should be raised.
		'''
		raise NotImplementedError('Subclasses of Check must implement this method')