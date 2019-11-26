

class Character(object):
	def __init__(self, id, water, name = '', controller = None, currentNodeID = None):
		self.id = id
		self.name = name
		self.water = water
		self.tags = []
		self.state = {}
		self.controller = controller
		self.currentNodeID = currentNodeID
		self.templateActions = []
		self.actions = []
	
	
	@property
	def currentNode(self):
		found =  self.water.lookupNode(self.currentNodeID)
		if found == None:
			raise RuntimeError('node with ID "{}" not found.'.format(self.currentNodeID))
		return found
		
		
	def setNode(self, id):
		self.currentNodeID = id
		
	def getTemplateActions(self):
		out = {}
		for templ in self.templateActions:
			out[templ.id] = templ
		return out