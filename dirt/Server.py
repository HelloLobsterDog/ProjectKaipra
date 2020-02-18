import logging

class Server(object):
	def __init__(self, saveLocation, debugModeOn = False):
		self.water = None
		self.saveLocation = saveLocation
		self.debugMode = debugModeOn
		self.logger = logging.getLogger('dirt.server')
		# transient - not saved when server shuts down:
		self.connectedClients = {} # userID : client object
		self.clientLanguages = {} # userID : lang
		# saved:
		self.clientCharacters = {} # userID : characterID
		
	def setWater(self, water):
		self.water = water
		water.server = self
	
	def load(self):
		''' Loads the saved data out of the save location and updates the Water to the saved state. '''
		pass # TODO
	
	def save(self):
		''' Takes all changes that have been made to the water and saves them out to the save location. '''
		pass # TODO
	
	def connect(self, client, userID, lang):
		'''
		Connects the client to the server, with the userID and lang.
		If the userID provided has a character already, you will inhabit that character, but if not, 
		a new character will be created for you at the entry point.
		'''
		self.connectedClients[userID] = client
		self.clientLanguages[userID] = lang
		# if no character, make one.
		if not userID in self.clientCharacters:
			char = self.water.enter()
			char.controller = userID
			self.clientCharacters[userID] = char.id
	
	def disconnect(self, userID):
		''' disconnects userID from server '''
		if userID in self.connectedClients:
			del self.connectedClients[userID]
			del self.clientLanguages[userID]
	
	def receive(self, userID, text):
		''' Called to handle text received from clients '''
		if not userID in self.connectedClients:
			raise RuntimeError("userID is not connected")
		
		if text.strip() == "":
			# if they're sending us nothing, we respond with the node text again.
			character = self.water.getCharacter(self.clientCharacters[userID])
			nodeText = character.getNodeLangText()
			self.send(userID, nodeText)
		else:
			# regular ol' request for action
			character = self.water.getCharacter(self.clientCharacters[userID])
			character.performCommandText(text, self.clientLanguages[userID])
			self.water.executeActions()
		
	def send(self, userID, langText):
		'''
		Convenience method which sends the langText to the userID, using whatever lang the user has configured when they connected.
		Formats the langText before sending.
		If the user is not currently connected, this method will do nothing.
		'''
		if userID in self.connectedClients:
			character = self.water.getCharacter(self.clientCharacters[userID])
			unformatted = langText.get(self.clientLanguages[userID], self.water.defaultLang)
			if unformatted != None:
				formatted = character.formatText(unformatted, self.clientLanguages[userID])
				self.connectedClients[userID].receive(formatted)
	