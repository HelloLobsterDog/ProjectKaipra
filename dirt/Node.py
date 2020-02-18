import logging

from .LangText import LangText
from .Action import Action
from .checks import checkFactory
from .xmlUtil import *

class Node(object):
	def __init__(self, xmlElement = None, defaultLang = None):
		self.id = None
		self.textBlock = LangText()
		self.checks = []
		self.actions = []
		self.state = {}
		self.templateActions = []
		
		self.defaultLang = defaultLang
		self.logger = logging.getLogger('dirt.node')
		
		if xmlElement != None:
			self.id = xmlElement.attrib.get('id', None)
			if self.id == None:
				raise BadXMLError('node tag is missing id attribute'.format(key))
			validateAttributes(xmlElement, ['id'], [])
			validateNoTextOrTail(xmlElement)
			
			self.logger.debug('creating node with ID %s', self.id.strip())
			
			sortedChildren = sortChildren(xmlElement, ['text_block', 'check', 'state_var', 'action', 'template_action'])
			if not 'text_block' in sortedChildren:
				raise RuntimeError('no text_block was found. At least one is required - what are you going to show the player?')
			
			for text_block in sortedChildren['text_block']:
				self.logger.debug('handling text_block')
				validateAttributes(text_block, [], ['lang'])
				validateNoTail(text_block)
				lang = text_block.get('lang', self.defaultLang)
				if lang != None:
					lang = lang.strip()
				else:
					lang = self.defaultLang
				if self.textBlock.hasText(lang):
					raise RuntimeError('text-block with language "{}" is present more than once.'.format(lang))
				self.addTextBlock(text_block.text.strip(), lang)
				
			for check in sortedChildren.get('check', []):
				self.logger.debug('handling check')
				self.addCheck(checkFactory(check, self.defaultLang))
			
			for stateVar in sortedChildren.get('state_var', []):
				self.logger.debug('handling state_var')
				validateNoChildren(stateVar)
				validateNoTextOrTail(stateVar)
				validateAttributes(stateVar, ['name', 'type', 'default'], [])
				self.state[stateVar.attrib['name']] = parseState(stateVar.attrib['name'], stateVar.attrib['type'], stateVar, self.logger)
			
			for action in sortedChildren.get('action', []):
				self.logger.debug('handling action tag')
				self.addAction(Action(action, self.defaultLang))
			
			for templateAction in sortedChildren.get('template_action', []):
				self.logger.debug('handling template action tag')
				self.addTemplateAction(TemplateAction(xml = templateAction, defaultLang = self.defaultLang))
			
	def addTextBlock(self, text, lang):
		self.textBlock.add(lang, text)
		
	def addCheck(self, check):
		self.checks.append(check)
		
	def addAction(self, action):
		self.actions.append(action)
		
	def addTemplateAction(self, action):
		self.templateActions.append(action)
		
	def getTemplateAction(self, id):
		for action in self.templateActions:
			if action.id == id:
				return action
		return None
		