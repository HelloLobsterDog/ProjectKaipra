import sys

from dirt.util import anglicize

class CommandLineInterface(object):
	def __init__(self, gamePlayer):
		self.game = gamePlayer
	
	def mainloop(self):
		# start loop by printing out the node text
		print(anglicize('\n' + self.game.displayNode()))
	
		while True:
			# get input
			userInput = input('\n>')
			# specialized input handling
			if userInput.strip() == '': # if they say nothing, print the node text again
				print(anglicize(self.game.displayNode()))
				continue
			if userInput.strip() == 'exit': # if they say exit, then exit
				return
			# general input handling
			output = self.game.handleInput(userInput)
			if output:
				# if we ran a command with output, just display that.
				for out in output:
					print(anglicize(out))
			else:
				# we ran a command without output
				print(anglicize('\n' + self.game.displayNode()))
	