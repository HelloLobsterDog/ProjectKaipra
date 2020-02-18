from ..xmlUtil import *

def checkFactory(tag, lang):
	validateAttributes(tag, ['name', 'type', 'based_on'], [])
	type = tag.attrib['type'].strip()
	
	if type == 'choice':
		return NotImplementedError('ChoiceCheck is not implemented.') # TODO: implement ChoiceCheck
	elif type == 'comparison':
		return NotImplementedError('ComparisonCheck is not implemented.') # TODO: implement ComparisonCheck
	elif type == 'bool':
		return NotImplementedError('BooleanCheck is not implemented.') # TODO: implement BooleanCheck
		
	else:
		raise BadXMLError('check type "' + type + '" not recongized')
