

class ActionEffect(object):
	''' Provides a template for the methods which need to be implemented by subclasses. '''
	
	def execute(self, character):
		raise RuntimeError('This method must be overridden by subclasses')