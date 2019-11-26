#!/usr/bin/env python

import sys
import argparse
import os.path
import logging
import codecs

import dirt

from dirt.template_actions.GoTemplateAction import GoTemplateAction

def TODO_removeMe(player):
	char = dirt.Character('viewpoint', player.water, currentNodeID = 'Rattlesnake Dormitories')
	char.templateActions.append(GoTemplateAction('go', {'en-us': ['go']}))
	char.templateActions.append(GoTemplateAction('look', {'en-us': ['look']}))
	char.templateActions.append(GoTemplateAction('listen', {'en-us': ['listen']}))
	char.templateActions.append(GoTemplateAction('smell', {'en-us': ['smell']}))
	char.templateActions.append(GoTemplateAction('pry', {'en-us': ['pry']}))
	char.templateActions.append(GoTemplateAction('lift', {'en-us': ['lift']}))
	char.templateActions.append(GoTemplateAction('enter', {'en-us': ['enter']}))
	player.water.addCharacter(char)

def findFilesToLoad(path):
	path = os.path.normpath(path)
	if os.path.isfile(path):
		yield path
	elif os.path.isdir(path):
		for subpath in os.listdir(path):
			fullSubpath = os.path.join(path, subpath)
			if os.path.isfile(fullSubpath):
				yield fullSubpath
	else:
		raise RuntimeError('Path is not a file or a directory. Does it exist?')

if __name__ == "__main__":
	# parse command line args
	parser = argparse.ArgumentParser(description="A program which runs MUDs")
	parser.add_argument('--debug_out', action="store_true", help="Prints debugging information to the console.")
	parser.add_argument('--log', action="store_true", help="Turns on logging to the ./logs/ directory, which will be created.")
	parser.add_argument('--lang', action='store', default='en-us', help="Specifies the language to use. If the language is not present, the default language of the water will be used. Defaults to en-us.")
	parser.add_argument('path', help='Path to the file or directory to load.')
	args = parser.parse_args()
	
	# make game player
	player = dirt.GamePlayer('viewpoint', args.lang)
	
	# parse the XML all at once
	parsers = []
	for toLoad in findFilesToLoad(args.path):
		parsers.append(dirt.XMLWaterParser(toLoad))
	
	# get water from the parsers
	for waterParser in parsers:
		player.addWater(waterParser.parse())
	
	TODO_removeMe(player)
	
	# make interface
	cli = dirt.CommandLineInterface(player)
	
	# play
	cli.mainloop()
	
	# we're done
	sys.exit(0)