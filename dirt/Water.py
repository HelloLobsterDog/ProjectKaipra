

class Water(object):
	'''
	The "hydrated" data used to run the game.
	You combine the dirt (the engine) with the water (this data), and you get a MUD. Aren't I clever hahahahahahahahahahahahahahahahahahahahha
	'''
	def __init__(self, defaultLang = 'en-us'):
		self.nodes = []
		self.characters = []
		self.defaultLang = defaultLang
		self.validationProblems = []
	
	def destroy(self):
		self.characters = []
	
	def merge(self, other):
		for node in other.nodes:
			self.addNode(node)
		for char in other.characters:
			self.addCharacter(car)
		if other.defaultLang != self.defaultLang:
			self.validationProblems.append('merged default lang "{}" does not match our default lang "{}"'.format(other.defaultLang, self.defaultLang))
		for problem in other.validationProblems:
			self.validationProblems.append(problem)
	
	
	def addNode(self, node):
		self.nodes.append(node)
	
	def getNode(self, id):
		for node in self.nodes:
			if node.id == id:
				return node
		return None
	
	def lookupNode(self, id):
		for node in self.nodes:
			if node.id == id:
				return node
		return None
		
	
	def addCharacter(self, char):
		self.characters.append(char)
		char.water = self
		
	def findCharactersWithTag(self, tag):
		for char in self.characters:
			if tag in char.tags:
				yield char
		
	def lookupCharacter(self, id):
		for char in self.characters:
			if char.id == id:
				return char
		return None
	