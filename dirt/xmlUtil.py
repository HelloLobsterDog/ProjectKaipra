'''
xmlUtil.py

The dumping ground for all the disconnected xml-parsing-related functions.
'''


class BadXMLError(RuntimeError):
	''' subclass of RuntimeError which indicates more or less the same thing, but is more specific '''
	pass
	
	
def validateHasText(element):
	''' If element does not have text, it raises an exception '''
	if element.text == None or element.text.strip() == '':
		raise BadXMLError('element "{}" requires text in the tag.'.format(element.tag))

def validateNoChildren(element):
	''' If element has any children, it raises an exception. '''
	if len(list(element)) > 0:
		raise BadXMLError('element "{}" does not allow children.'.format(element.tag))

def sortChildren(element, allowedTags):
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

def validateNoAttributes(element):
	''' If element has any attributes, it raises an exception. '''
	if len(element.attrib) > 0:
		raise BadXMLError('element "{}" does not allow attributes.'.format(element.tag))

def validateAttributes(element, required, optional):
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

def validateNoTextOrTail(element):
	''' If element has any text or tail, it raises an exception. '''
	if element.text != None:
		if element.text.strip() != '':
			raise BadXMLError('text found inside an element ({}) which does not allow it.'.format(element.tag))
	if element.tail != None:
		if element.tail.strip() != '':
			raise BadXMLError('text found after an element ({}) which does not allow it.'.format(element.tag))

def validateNoTail(element):
	''' If element has any tail, it raises an exception. '''
	if element.tail != None:
		if element.tail.strip() != '':
			raise BadXMLError('text found after an element which does not allow it.')

def parseThenText(element, defaultLang):
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
			
			validateNoChildren(child)
			validateNoTail(child)
			for attrib in child.attrib:
				if attrib.strip() != 'lang' and attrib.strip() != 'formatted':
					raise BadXMLError('attribute of then tag "{}" not recognized'.format(attrib))
			langs.append((child.text.strip(), lang.strip(), formatted))
	return langs

def parseState(name, type, tag, logger = None):
	''' taking the name, type and tag of a state_var tag, this method parses and returns it's default value. '''
	if logger == None:
		logger = logging.getLogger('dirt.default_state')
	# each different state_var type will end up using different code to instantiate it
	if type == 'integer':
		logger.debug('state var "%s" is type integer.', name)
		try:
			val = int(tag.attrib['default'])
			return val
		except Exception as e:
			raise BadXMLError('Could not parse text value "{}" into an integer in state_var'.format(tag.attrib['default']))
		
	elif type == 'boolean':
		logger.debug('state var "%s" is type boolean.', name)
		if not tag.attrib['default'].lower() in ['true', 'false']:
			raise BadXMLError('boolean value for state_var not recognized: {}'.format(tag.attrib['default']))
		val = tag.attrib['default'].lower() == 'true'
		return val
		
	elif type == 'decimal':
		logger.debug('state var "%s" is type decimal.', name)
		try:
			val = float(tag.attrib['default'])
			return val
		except Exception as e:
			raise BadXMLError('Could not parse text value "{}" into an integer in state_var'.format(tag.attrib['default']))
		
	else:
		raise BadXMLError('state_var type not recognized: {}'.format(type))