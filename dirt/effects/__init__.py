from .BadCommandTextEffect import BadCommandTextEffect
from .DisplayTextEffect import DisplayTextEffect
from .ChangeNodeEffect import ChangeNodeEffect
from .DisplayNodeTextEffect import DisplayNodeTextEffect
from .SetVarEffect import SetVarEffect

from ..xmlUtil import *

def effectFactory(tag, lang):
	validateNoTail(tag)
	if 'type' in tag.attrib:
		type = tag.attrib['type'].strip()
		
		if type == 'display_text':
			return DisplayTextEffect(xml = tag)
		elif type == 'print_node_text':
			return DisplayNodeTextEffect(xml = tag)
		elif type == 'change_node':
			return ChangeNodeEffect(xml = tag)
		elif type == 'set_var':
			return SetVarEffect(xml = tag)
		elif type == 'bad_command':
			return BadCommandTextEffect(xml = tag)
		
		else:
			raise BadXMLError('effect type "{}" is not recognized.'.format(type))
	else:
		raise BadXMLError('action effect has no type.')
