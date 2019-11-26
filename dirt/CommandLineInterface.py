import sys

from dirt.util import anglicize

class CommandLineInterface(object):
	def __init__(self, gamePlayer):
		self.game = gamePlayer
	
	def mainloop(self):
		while True:
			# display text
			print(anglicize('\n' + self.game.displayNode()))
			# get input
			userInput = input('\n>')
			# specialized input handling
			if userInput.strip() == 'exit':
				return
			# general input handling
			output = self.game.handleInput(userInput)
			for out in output:
				print(anglicize(out))
	