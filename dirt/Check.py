

class Check(object):
	''' This class exists to exhibit the interface required to be implemented by subclasses. '''
	def __init__(self):
		self.name = None
		
	def getText(self, stateDict):
		raise RuntimeError('subclasses must override this method')