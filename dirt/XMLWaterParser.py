import xml.etree.ElementTree as ET
import logging

from dirt.Water import Water
from dirt.Node import Node
from dirt.BooleanCheck import BooleanCheck
from dirt.ChoiceCheck import ChoiceCheck
from dirt.ComparisonCheck import ComparisonCheck
from dirt.Action import Action
from dirt.ActionTrigger import ActionTrigger

from dirt.action_effects.ChangeNodeEffect import ChangeNodeEffect
from dirt.action_effects.DisplayTextEffect import DisplayTextEffect
from dirt.action_effects.SetVarEffect import SetVarEffect

class BadXMLError(RuntimeError):
	''' subclass of RuntimeError which indicates more or less the same thing, but is more specific '''
	pass

class XMLWaterParser(object):
	def __init__(self, filename = None, fromString = None, defaultLang = 'en-us'):
		self.defaultLang = defaultLang
		self.logger = logging.getLogger('XMLWaterParser')
		
		if filename != None:
			if fromString != None:
				raise ValueError('both filename and fromString are provided. Only one is allowed.')
			self.logger.debug('parsing xml from filename: %s', filename)
			self.root = ET.parse(filename).getroot()
		elif fromString != None:
			if filename != None:
				raise ValueError('both filename and fromString are provided. Only one is allowed.')
			self.logger.debug('parsing xml from string.')
			self.root = ET.fromstring(fromString)
		else:
			raise ValueError('Neither filename and fromString are provided. Must provide one.')
		self.logger.info('XML parsed to tree successfully.')
	
	def parse(self):
		''' parses the XML tree into a Water instance, and returns it. '''
		# validate root tag itself
		defaultLang = self.defaultLang
		if self.root.tag != 'water':
			raise BadXMLError('Root tag name "{}" is not recognized'.format(self.root.tag))
		if 'default_lang' in self.root.attrib:
			defaultLang = self.root.attrib['default_lang']
		self._validateAttributes(self.root, [], ['default_lang'])
		self.logger.debug('using default_lang %s', defaultLang)
		
		# it's valid.
		output = Water(defaultLang)
		nodeCount = 0
		
		# look at the children
		for index, child in enumerate(self.root):
			if child.tag == 'node':
				self.logger.debug('parsing node tag #%d', index)
				nodeCount += 1
				try:
					output.addNode(self._handleNode(child, defaultLang))
				except BadXMLError as e:
					self.logger.exception('Node #{} has failed to parse due to the XML being invalid. Processing of other nodes will continue in an attempt to show you as many errors at once as possible.'.format(nodeCount))
					
			elif child.tag == 'bad_command_error_text':
				self.logger.debug('parsing badCommandErrorText tag (#%d)', index)
				self._validateAttributes(child, [], ['lang'])
				self._noTail(child)
				self._noChildren(child)
				output.addBadCommandText(child.text.strip(), child.attrib.get('lang', None))
				
			else:
				raise BadXMLError('child tag #{} of root named "{}" not recognized'.format(index + 1, child.tag))
		
		return output
		
	def _handleNode(self, nodeTag, defaultLang):
		id = nodeTag.attrib.get('id', None)
		if id == None:
			raise BadXMLError('node tag is missing id attribute'.format(key))
		self._validateAttributes(nodeTag, ['id'], [])
		self._noTextOrTail(nodeTag)
		
		node = Node(id.strip())
		self.logger.debug('creating node with ID %s', id.strip())
		
		sortedChildren = self._sortChildren(nodeTag, ['text_block', 'check', 'state_var', 'action'])
		if not 'text_block' in sortedChildren:
			node.problems.append('no text_block was found. At least one is required - what are you going to show the player?')
		
		for text_block in sortedChildren['text_block']:
			self.logger.debug('handling text_block')
			self._validateAttributes(text_block, [], ['lang'])
			self._noTail(text_block)
			lang = text_block.get('lang', defaultLang).strip()
			if node.hasText(lang):
				node.problems.append('text-block with language "{}" is present more than once.'.format(lang))
			node.addText(text_block.text.strip(), lang)
			
		for check in sortedChildren.get('check', []):
			self.logger.debug('handling check')
			self._noTextOrTail(check)
			self._validateAttributes(check, ['name', 'type', 'based_on'], [])
			type = check.attrib['type'].strip()
			# each check type has a different method to create the Check instance
			if type == 'choice':
				node.addCheck(self._handleChoiceCheck(check.attrib['name'].strip(), check.attrib['based_on'].strip(), check, defaultLang))
			elif type == 'comparison':
				node.addCheck(self._handleComparisonCheck(check.attrib['name'].strip(), check.attrib['based_on'].strip(), check, defaultLang))
			elif type == 'bool':
				node.addCheck(self._handleBoolCheck(check.attrib['name'].strip(), check.attrib['based_on'].strip(), check, defaultLang))
			else:
				raise BadXMLError('check type "{}" is not recognized'.format(type))
		
		for stateVar in sortedChildren.get('state_var', []):
			self.logger.debug('handling state_var')
			self._noChildren(stateVar)
			self._noTextOrTail(stateVar)
			self._validateAttributes(stateVar, ['name', 'type', 'default'], [])
			node.state[stateVar.attrib['name']] = self._handleState(stateVar.attrib['name'], stateVar.attrib['type'], stateVar)
		
		for action in sortedChildren.get('action', []):
			self.logger.debug('handling action tag')
			self._noTextOrTail(action)
			self._noAttributes(action)
			actionChildren = self._sortChildren(action, ['trigger', 'effect'])
			
			createdAction = Action()
			node.addAction(createdAction)
			
			for trigger in actionChildren['trigger']:
				createdAction.addTrigger(self._handleActionTrigger(trigger, defaultLang))
				
			for effect in actionChildren['effect']:
				createdAction.addEffect(self._handleActionEffect(effect, defaultLang))
		
		return node
		
	def _handleActionTrigger(self, tag, defaultLang):
		''' Taking a trigger tag, this method parses it into a usable object and returns it. '''
		self._noTail(tag)
		self._noChildren(tag)
		self._validateAttributes(tag, [], ['equivalent', 'target_for', 'lang'])
		
		contents = tag.text
		if contents == None:
			raise BadXMLError('Trigger tag has no text. What triggers it?')
		contents = contents.strip()
		lang = tag.attrib.get('lang', defaultLang).strip()
		checkedActions = []
		requiredActions = []
		if 'equivalent' in tag.attrib:
			checkedActions.append(tag.attrib['equivalent'].strip())
		if 'target_for' in tag.attrib:
			val = tag.attrib['target_for'].strip()
			requiredActions.append(val)
			checkedActions.append(val)
		
		# have everything we need. Put together trigger and return it.
		return ActionTrigger(contents, requiredActions, checkedActions, lang)
	
	def _handleActionEffect(self, tag, defaultLang):
		''' Taking an effect tag, this method parses it into a usable effect, and returns it. '''
		self._noTail(tag)
		if 'type' in tag.attrib:
			type = tag.attrib['type'].strip()
			
			if type == 'display_text':
				self._validateAttributes(tag, ['type'], ['lang', 'formatted'])
				self._noChildren(tag)
				displayedText = tag.text
				if displayedText == None:
					raise BadXMLError('display_text effect tag has no text. What triggers it?')
				lang = tag.attrib.get('lang', defaultLang)
				formatted = tag.attrib.get('formatted', 'false').strip()
				if not formatted.lower() in ['true', 'false']:
					raise BadXMLError('value for property formatted "{}" is not valid. Must be true or false.'.format(formatted))
				formatted = formatted.lower() == 'true'
				return DisplayTextEffect(displayedText.strip(), lang.strip(), formatted)
			
			elif type == 'change_node':
				self._validateAttributes(tag, ['type'], []) # no more attributes
				self._noChildren(tag)
				changeTo = tag.text
				if changeTo == None:
					raise BadXMLError('Change node effect has no text. What node will it change to?')
				return ChangeNodeEffect(changeTo.strip())
				
			elif type == 'set_var':
				self._validateAttributes(tag, ['type', 'var'], [])
				self._noChildren(tag)
				value = tag.text
				if value == None:
					raise BadXMLError('set var effect has no text. What will it be set to?')
				varName = tag.attrib['var'].strip()
				return SetVarEffect(varName, value.strip())
			
			else:
				raise BadXMLError('effect type "{}" is not recognized.'.format(type))
		else:
			raise BadXMLError('type attribute is missing from effect tag.')
	
	def _handleState(self, name, type, tag):
		''' taking the name, type and tag of a state_var tag, this method parses and returns it's default value. '''
		# each different state_var type will end up using different code to instantiate it
		if type == 'integer':
			self.logger.debug('state var "%s" is type integer.', name)
			try:
				val = int(tag.attrib['default'])
				return val
			except Exception as e:
				raise BadXMLError('Could not parse text value "{}" into an integer in state_var'.format(tag.attrib['default']))
			
		elif type == 'boolean':
			self.logger.debug('state var "%s" is type boolean.', name)
			if not tag.attrib['default'].lower() in ['true', 'false']:
				raise BadXMLError('boolean value for state_var not recognized: {}'.format(tag.attrib['default']))
			val = tag.attrib['default'].lower() == 'true'
			return val
			
		elif type == 'decimal':
			self.logger.debug('state var "%s" is type decimal.', name)
			try:
				val = float(tag.attrib['default'])
				return val
			except Exception as e:
				raise BadXMLError('Could not parse text value "{}" into an integer in state_var'.format(tag.attrib['default']))
			
		else:
			raise BadXMLError('state_var type not recognized: {}'.format(type))
		
	def _handleChoiceCheck(self, name, based_on, tag, defaultLang):
		'''
		Parses the tag passed into a choice check, and returns the check.
		example:
		<check name="favorite_vowel" type="choice" based_on="node.vowel">
			<option> <if> 0 </if> <then> a </then> </option>
			<option> <if> 1 </if> <then> e </then> </option>
			<option> <if> 2 </if> <then> i </then> </option>
			<option> <if> 3 </if> <then> o </then> </option>
			<option> <if> 4 </if> <then> u </then> </option>
			<option> </anything_else> <then> y </then> </option>
		</check>
		'''
		self.logger.debug('handling choice check with name "%s" and based_on "%s"', name, based_on)
		output = ChoiceCheck(name, based_on)
		sortedChildren = self._sortChildren(tag, ['option'])
		for option in sortedChildren['option']:
			self._noAttributes(option)
			self._noTextOrTail(option)
			sortedOptionChildren = self._sortChildren(option, ['if', 'then', 'anything_else'])
			ifs = []
			for ifTag in sortedOptionChildren.get('if', []):
				self._noAttributes(ifTag)
				self._noTail(ifTag)
				self._noChildren(ifTag)
				ifs.append(ifTag.text.strip())
			for anything in sortedOptionChildren.get('anything_else', []):
				self._noAttributes(anything)
				self._noTextOrTail(anything)
				self._noChildren(anything)
				ifs.append(None) # None means that the choice accepts anything
			# ifs are done, so we can now use them to add the thens
			thens = self._getThenText(option, defaultLang)
			if len(thens) < 1:
				raise BadXMLError('at least one then tag is required for each option (otherwise why include it?)')
			for then in thens:
				output.addTextForValues(ifs, then[0], then[1], then[2])
		return output
		
	def _handleComparisonCheck(self, name, based_on, tag, defaultLang):
		'''
		Parses the tag passed into a comparison check, and returns the check.
		
		example:
		<check name="weight_abbreviation" type="comparison" based_on="node.weight">
			<option> <less_than> 4.2 </less_than> <then> lb </then> </option>
			<option> <equal> 4.2 </equal> <then> g </then> </option>
			<option> <greater_than> 4.2 </greater_than> <then> kg </then> </option>
		</check>
		'''
		self.logger.debug('handling comparison check with name "%s" and based_on "%s"', name, based_on)
		output = ComparisonCheck(name, based_on)
		sortedChildren = self._sortChildren(tag, ['option'])
		for option in sortedChildren['option']:
			self._noAttributes(option)
			self._noTextOrTail(option)
			# put together the list of comparisons
			comparisons = []
			sortedOptionChildren = self._sortChildren(option, ['then', 'less_than', 'less_than_or_equal', 'equal', 'greater_than_or_equal', 'greater_than'])
			if 'then' in sortedOptionChildren:
				del sortedOptionChildren['then'] # we only care about the comparisons for this step
			for key in sortedOptionChildren:
				for comparisonTag in sortedOptionChildren[key]:
					comparisons.append(self._handleComparisonCheckComparison(comparisonTag))
				
			# ifs are done, so we can now use them to add the thens
			thens = self._getThenText(option, defaultLang)
			if len(thens) < 1:
				raise BadXMLError('at least one then tag is required for each option (otherwise why include it?)')
			for then in thens:
				output.addOutput(comparisons, then[0], then[1], then[2])
		return output
	
	def _handleComparisonCheckComparison(self, tag):
		'''
		Takes a tag from a comparison check which contains one of the comparison operations, and returns
		an instantiated comparison to pass to addOutput of ComparisonCheck.
		
		examples:
		<less_than> 4.2 </less_than>
		<equal> 4.2 </equal>
		'''
		self._noAttributes(tag)
		self._noChildren(tag)
		self._noTail(tag)
		# figure out comparison type
		comparisonType = None
		if tag.tag == 'less_than':
			comparisonType = ComparisonCheck.LESS_THAN
		elif tag.tag == 'less_than_or_equal':
			comparisonType = ComparisonCheck.LESS_THAN_OR_EQUAL
		elif tag.tag == 'equal':
			comparisonType = ComparisonCheck.EQUAL
		elif tag.tag == 'greater_than':
			comparisonType = ComparisonCheck.GREATER_THAN_OR_EQUAL
		elif tag.tag == 'greater_than_or_equal':
			comparisonType = ComparisonCheck.GREATER_THAN
		else:
			raise ValueError('tag name "{}" is not recognized in this method. Caller should not have passed it.'.format(tag.tag))
		# Figure out value. We're expecting a numeric type, but we don't know what.
		value = None
		# to determine what type it is, we just try the int and float constructors and if they blow up it's not that type.
		try:
			value = int(tag.text.strip())
		except Exception as e:
			# well, it's not an integer...
			try:
				value = float(tag.text.strip())
			except Exception as e2:
				# and it's not a float...
				# which means we don't know what it is, so blow up
				raise BadXMLError('comparison value "{}" is not an integer or a float.'.format(tag.text.strip()))
		
		return ComparisonCheck.Comparison(comparisonType, value)
		
	def _handleBoolCheck(self, name, based_on, tag, defaultLang):
		'''
		Parses the tag passed into a bool check, and returns the check.
		
		example:
		<check name="win_or_loss" type="bool" based_on="node.victory">
			<true> <then> w </then> </true>
			<false> <then> l </then> </false>
		</check>
		'''
		self.logger.debug('handling boolean check with name "%s" and based_on "%s"', name, based_on)
		output = BooleanCheck(name, based_on)
		foundTrue = False
		foundFalse = False
		for child in tag:
			if child.tag == 'true':
				if foundTrue:
					raise BadXMLError('true tag found more than once. The bool check must have exactly 2 tags (true and false) and no more.')
				foundTrue = True
				# handle the true tag
				self._noAttributes(child)
				self._noTextOrTail(child)
				self._sortChildren(child, ['then'])
				texts = self._getThenText(child, defaultLang)
				for text in texts:
					output.addOutput(True, text[0], text[1], text[2])
				
			elif child.tag == 'false':
				if foundFalse:
					raise BadXMLError('false tag found more than once. The bool check must have exactly 2 tags (true and false) and no more.')
				foundFalse = True
				# handle the false tag
				self._noAttributes(child)
				self._noTextOrTail(child)
				self._sortChildren(child, ['then'])
				texts = self._getThenText(child, defaultLang)
				for text in texts:
					output.addOutput(False, text[0], text[1], text[2])
				
			else:
				raise BadXMLError('tag "{}" is not recognized as a child of bool checks.'.format(child.tag))
		if not foundTrue:
			raise BadXMLError('true tag is required for boolean checks, but is not present')
		if not foundFalse:
			raise BadXMLError('false tag is required for boolean checks, but is not present')
		return output
		
		
	
	def _noChildren(self, element):
		''' If element has any children, it raises an exception. '''
		if len(list(element)) > 0:
			raise BadXMLError('element "{}" does not allow children.'.format(element.tag))
	
	def _sortChildren(self, element, allowedTags):
		'''
		Takes all the children tags out of the element, and sorts them into lists based on what their tag name is.
		If any tags are present as children, but their tag name is not present in the allowedTags list, it will fail.
		'''
		sortedChildren = {}
		for child in element:
			if child.tag in allowedTags:
				sortedChildren.setdefault(child.tag, []).append(child)
			else:
				raise BadXMLError('child tag "{}" is not allowed in tag "{}"'.format(child.tag, element.tag))
		return sortedChildren
	
	def _noAttributes(self, element):
		''' If element has any attributes, it raises an exception. '''
		if len(element.attrib) > 0:
			raise BadXMLError('element "{}" does not allow attributes.'.format(element.tag))
	
	def _validateAttributes(self, element, required, optional):
		'''
		Reads all the attributes of the element, and ensures that all of them are either in the required or optional lists.
		For all attribute names in the required list, if any of them are not present on the element, it will fail.
		'''
		for attrib in element.attrib:
			if not attrib.strip() in required and not attrib.strip() in optional:
				raise BadXMLError('Attribute "{}" not recongized on tag "{}"'.format(attrib.strip(), element.tag))
		for req in required:
			if not req.strip() in element.attrib:
				raise BadXMLError('Required attribute "{}" not found on tag "{}"'.format(req.strip(), element.tag))
	
	def _noTextOrTail(self, element):
		''' If element has any text or tail, it raises an exception. '''
		if element.text != None:
			if element.text.strip() != '':
				raise BadXMLError('text found inside an element ({}) which does not allow it.'.format(element.tag))
		if element.tail != None:
			if element.tail.strip() != '':
				raise BadXMLError('text found after an element ({}) which does not allow it.'.format(element.tag))
	
	def _noTail(self, element):
		''' If element has any tail, it raises an exception. '''
		if element.tail != None:
			if element.tail.strip() != '':
				raise BadXMLError('text found after an element which does not allow it.')
	
	def _getThenText(self, element, defaultLang):
		'''
		Takes all the children tags of element which have the name 'then',
		takes their text block values and puts them into a list, in the form of tuples containing (text, lang, formatted)
		If the lang of the then tag is not specified, it will be defaultLang.
		If the formatted attribute is provided, it will be parsed, and if not, it defaults to False.
		'''
		langs = []
		for child in element:
			if child.tag == 'then':
				lang = child.attrib.get('lang', defaultLang)
				
				formatted = child.attrib.get('formatted', 'false').strip()
				if not formatted.lower() in ['true', 'false']:
					raise BadXMLError('value for property formatted "{}" is not valid. Must be true or false.'.format(formatted))
				formatted = formatted.lower() == 'true'
				
				self._noChildren(child)
				self._noTail(child)
				for attrib in child.attrib:
					if attrib.strip() != 'lang' and attrib.strip() != 'formatted':
						raise BadXMLError('attribute of then tag "{}" not recognized'.format(attrib))
				langs.append((child.text.strip(), lang.strip(), formatted))
		return langs
				
