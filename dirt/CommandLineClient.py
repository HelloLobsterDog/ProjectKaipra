from .Client import Client
from .util import anglicize

class CommandLineClient(Client):
	
	def receive(self, text):
		self.logger.debug('received text from server: %s', text)
		print(anglicize('\n' + text.strip()))
	
	def mainloop(self):
		if self.server == None:
			raise RuntimeError("have not connected to a server yet. Cannot start mainloop")
		
		self.send("")
		
		while True:
			userInput = input("\n>")
			if userInput.strip() == 'exit': # if they say exit, then exit
				self.logger.info('Disconnecting at user request.')
				self.disconnect()
				return
			else:
				self.send(userInput)
	