import xml.etree.ElementTree as ET
import logging

from .xmlUtil import *
from .LangText import LangText
from .Node import Node
from .Character import Character
from .TemplateAction import TemplateAction
from .SkillTree import SkillTree

class Water(object):
	def __init__(self, server = None, xmlFilePath = None, xmlString = None):
		self.defaultLang = None
		self.badCommandText = LangText()
		self.nodes = []
		self.characters = []
		self.templateActions = []
		self.skillTrees = []
		
		self.charactersWithActions = []
		self.validationIssues = []
		
		self.logger = logging.getLogger('dirt.water')
		self.server = server
		
		if xmlFilePath != None:
			if xmlString != None:
				raise ValueError('both xmlFilePath and xmlString are provided. Only one is allowed.')
			self.logger.info('parsing xml from filename: %s', xmlFilePath)
			try:
				root = ET.parse(xmlFilePath).getroot()
			except Exception as e:
				self.logger.exception('Exception encountered while reading XML file {} due to an XML syntax error.'.format(xmlFilePath))
				raise
			else:
				self.logger.info('XML is syntactically valid. Converting to Water object...')
			self.fromElement(root)
		elif xmlString != None:
			if xmlFilePath != None:
				raise ValueError('both xmlFilePath and xmlString are provided. Only one is allowed.')
			self.logger.info('parsing xml from string (length %d characters).', len(xmlString))
			try:
				root = ET.fromstring(xmlString)
			except Exception as e:
				self.logger.exception('Exception encountered while reading XML from string. XML in the string is syntactically invalid.')
				raise
			else:
				self.logger.info('XML is syntactically valid. Converting to Water object...')
			self.fromElement(root)
	
	def fromElement(self, root):
		''' Taking an element tree instance, this method "hydrates" the Water instance with data from the xml '''
		try:
			if root.tag != 'water':
				raise BadXMLError('Root tag name "{}" is not recognized'.format(root.tag))
			if 'default_lang' in root.attrib:
				self.defaultLang = root.attrib['default_lang']
			validateAttributes(root, [], ['default_lang'])
			self.logger.debug('using default_lang %s', self.defaultLang)
			
			# look at the children
			allGood = True
			for index, child in enumerate(root):
				if child.tag == 'node':
					self.logger.debug('parsing node tag #%d', index)
					try:
						self.addNode(Node(xmlElement = child, defaultLang = self.defaultLang))
					except BadXMLError as e:
						allGood = False
						self.logger.exception('Node #{} has failed to parse due to the XML being syntactically correct, but invalid. Processing of other nodes will continue in an attempt to show you as many errors at once as possible.'.format(index + 1))
						
				elif child.tag == 'bad_command_error_text':
					self.logger.debug('parsing badCommandErrorText tag (#%d)', index + 1)
					validateAttributes(child, [], ['lang'])
					validateNoTail(child)
					validateNoChildren(child)
					self.badCommandText.add(child.attrib.get('lang', self.defaultLang), child.text.strip())
				
				elif child.tag == 'template_action':
					self.logger.debug('parsing template action tag (#%d)', index + 1)
					self.addTemplateAction(TemplateAction(xml = child, defaultLang = self.defaultLang))
					
				elif child.tag == 'skill_tree':
					self.logger.debug("parsing skill tree tag (#%d)", index + 1)
					self.addSkillTree(SkillTree(element = child, defaultLang = self.defaultLang))
					
				else:
					raise BadXMLError('child tag #{} of root named "{}" not recognized'.format(index + 1, child.tag))
					
			if not allGood:
				raise BadXMLError('At least one bad node was found in the xml. See further up in the logs for the error message(s)')
		except BadXMLError as e:
			self.logger.exception('XML is does not have syntax errors, but is not valid Water data due to exception')
			raise
		except Exception as e:
			self.logger.exception('non-BadXMLError exception encountered while attempting to parse XML tree to water.')
			raise
			
	
	def validate(self):
		''' Validates that all pieces of the Water are free of error, and places validation problems into the water's list. '''
		pass
		# actions which lack any triggers or any effects
		# nodes which lack exits
		# nodes with references to checks that don't exist
		# change to nodes which don't exist
		# invalid check names (check names must be valid python variable names)
		# characters not in nodes
		# duplicate action triggers (2 things responding to the same thing)
		# duplicate ids: character, node, template action, checks
		# action triggers which are upper case
		# find things that lack text in the default language
		# total up all languages, and find cases where bad command error text does not cover all the languages (including default)
		# total up all languages, and find things within the water which lack translation into all languages
		# skills with prerequisites actually point to ids that exist
	
	
	def setServer(self, server):
		server.water = self
		self.server = server
		
	def markCharacterHasActions(self, character):
		self.charactersWithActions.append(character)
		
	def executeActions(self):
		newVersionOfList = []
		for character in self.charactersWithActions:
			character.executeEffects()
			if character.hasQueuedEffects():
				newVersionOfList.append(character)
		self.charactersWithActions = newVersionOfList
		
	def getCharacter(self, characterID):
		''' Looks up the character with the ID provided and returns it, or None if no such character exists. '''
		for char in self.characters:
			if char.id == characterID:
				return char
		return None
	
	def addCharacter(self, character):
		for char in self.characters:
			if char.id == character.id:
				raise RuntimeError('Character id %s is duplicated'.format(char.id))
		# add
		self.characters.append(character)
		character.water = self
		if character.hasQueuedEffects():
			self.markCharacterHasActions(character)
		
	def enter(self): # TODO make this a real thing
		'''
		Called to create a new character at the entry point of the game.
		Returns the new character created.
		'''
		character = Character(owningWater = self)
		character.id = 'player'
		character.currentNodeID = "Rattlesnake Dormitories"
		self.addCharacter(character)
		return character
	
	def merge(self, other):
		''' Merges all the content from the passed water instance into this one. '''
		self.logger.info('Merging water with %d nodes, %d characters and %d template actions', len(other.nodes), len(other.characters), len(other.templateActions))
		try:
			# default lang
			if self.defaultLang != None and other.defaultLang != None and other.defaultLang != self.defaultLang:
				raise RuntimeError('merged water has default language "{}" which differs from ours "{}"'.format(other.defaultLang, self.defaultLang))
			# bad command text
			self.badCommandText.merge(other.badCommandText, overwriteExisting = False)
			# nodes
			for node in other.nodes:
				self.addNode(node)
			# characters
			for character in other.characters:
				self.addCharacter(character)
			# template actions
			for ta in other.templateActions:
				self.addTemplateAction(ta)
		except Exception as e:
			self.logger.exception('Exception encountered while merging Water instances.')
		
	def addNode(self, node):
		# check for duplicates
		for child in self.nodes:
			if child.id == node.id:
				raise RuntimeError('Node name %s is duplicated'.format(node.id))
		# add
		self.nodes.append(node)
	
	def getNode(self, id):
		for child in self.nodes:
			if child.id == id:
				return child
		return None
		
	def addTemplateAction(self, action):
		self.templateActions.append(action)
	
	def getTemplateAction(self, id):
		for action in self.templateActions:
			if action.id == id:
				return action
		return None
	
	def getSkillTree(self, id):
		for skillTree in self.skillTrees:
			if skillTree.id == id:
				return skillTree
		return None
	
	def addSkillTree(self, skillTree):
		self.skillTrees.append(skillTree)