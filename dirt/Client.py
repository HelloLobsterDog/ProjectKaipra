import logging

class Client(object):
	'''
	Superclass for all client implementations. Provides much of the boilerplate involved in interacting with servers,
	but much of the meat of the client/server interaction is handled by subclasses.
	'''
	def __init__(self, userID, lang):
		self.userID = userID
		self.lang = lang
		self.server = None
		
		self.logger = logging.getLogger('dirt.client')
	
	def connect(self, server):
		self.server = server
		self.logger.debug('connecting to server: %s', server)
		self.server.connect(self, self.userID, self.lang)
		self.logger.info('connected successfully.')
	
	def disconnect(self):
		if self.server != None:
			self.logger.debug('disconnecting from server')
			self.server.disconnect(self.userID)
			self.server = None
			self.logger.debug('disconnected successfully')
	
	def send(self, text):
		if self.server == None:
			raise RuntimeError("Cannot send, because we are not connected to a server.")
		self.logger.debug('sending server text: %s', text)
		self.server.receive(self.userID, text)
		
	def receive(self, text):
		raise RuntimeError("this method must be overridden")
	