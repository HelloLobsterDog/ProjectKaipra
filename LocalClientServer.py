#!/usr/bin/env python

import sys
import argparse
import os.path
import logging
import logging.handlers

from dirt.CommandLineClient import CommandLineClient
from dirt.Server import Server
from dirt.Water import Water


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
	parser.add_argument('--debug_out', action="store_true", help="Prints debugging information in addition to typical gameplay text.")
	parser.add_argument('--log', action="store_true", help="Turns on logging to the ./logs/ directory, which will be created.")
	parser.add_argument('--lang', action='store', default='en-us', help="Specifies the language to use. If the language is not present, the default language of the water will be used. Defaults to en-us.")
	parser.add_argument('--save_path', action='store', default='./saves/', help="Path to the directory in which to save data for the game. Defaults to ./saves/")
	parser.add_argument('path', help='Path to the xml file (or directory containing XML files) to load.')
	args = parser.parse_args()
	
	# setup logging
	if args.log:
		os.makedirs('./logs/', exist_ok = True)
		logger = logging.getLogger('dirt')
		logging.root = logger
		logger.setLevel(logging.DEBUG)
		formatter = logging.Formatter('%(asctime)s [%(levelname)-5s] %(name)s: %(message)s')
		fh = logging.handlers.TimedRotatingFileHandler('./logs/dirt.log', when = 'midnight', encoding = 'utf-8')
		fh.setFormatter(formatter)
		fh.setLevel(logging.DEBUG)
		logger.addHandler(fh)
		logger.info('Beginning combined local client/server instance.')
	else:
		# Logging off. We do still set up the logger, but it doesn't write anywhere, and is essentially "off" because of the level
		logger = logging.getLogger('dirt')
		logger.setLevel(logging.CRITICAL)
	
	# create client
	client = CommandLineClient('player', args.lang)
	# create server
	server = Server(args.save_path, args.debug_out)
	# load water
	server.logger.info('Loading Water...')
	water = Water(server)
	error = False
	for toLoad in findFilesToLoad(args.path):
		try:
			loaded = Water(server, toLoad)
			water.merge(loaded)
		except Exception as e:
			error = True # swallow. Log is done within method.
	server.setWater(water)
	if error:
		server.logger.error('Error encountered while loading water. Exiting early.\n')
		print('At least one error encountered while loading water. See logs for full details.')
		sys.exit(3)
	server.logger.info('Water loaded. Validating...')
	# validate water
	try:
		server.water.validate()
	except Exception as e:
		server.logger.error('Error encountered while validating water. Exiting early.\n')
		print('Error encountered while validating water. See logs for full details.')
		sys.exit(4)
	server.logger.info('Water validated.')
	# load save data
	try:
		server.load()
	except Exception as e:
		server.logger.error('Error encountered while loading save data. Exiting early.\n')
		print('Exception encountered while loading save data. Full details in the logs.')
		sys.exit(5)
	# knit client and server together
	client.connect(server)
	
	# game takes place
	client.logger.info('Client mainloop beginning. Game will now take place:\n')
	try:
		client.mainloop()
	except Exception as e:
		client.logger.exception('Exception in client mainloop.')
		print('Exception encountered while running the game (full details are in the logs): ' + str(e) + "\n")
		sys.exit(6)
	client.logger.info('Client mainloop has ended. Shutting down.')
	
	# game is over. Disconnect.
	client.disconnect()
	# save
	try:
		server.save()
	except Exception as e:
		server.logger.error('Error encountered while saving save data.\n')
		print('Exception encountered while saving save data. Full details in the logs.')
		sys.exit(7)
	
	client.logger.info('Local client shut down successfully.\n')
	sys.exit(0) # successfully completed