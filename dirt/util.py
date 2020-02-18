import codecs

ANGLICIZE_DICT = {'“':'"', '”':'"', '’':"'"}

def replaceChars(text, charDict):
	for char in text:
		yield charDict.get(char, char)

def anglicize(text, reencode = True):
	replaced = ''.join(replaceChars(text, ANGLICIZE_DICT))
	if reencode:
		return codecs.encode(replaced, 'ascii', errors = 'replace').decode('ascii')
	else:
		return replaced



def parseMatchTypes(text, matchTo):
	if isinstance(matchTo, str):
		return str(text)
	elif isinstance(matchTo, bool):
		if not text.strip().lower() in ['true', 'false']:
			raise RuntimeError('text being parsed to bool "{}" is not true or false.'.format(text))
		return text.strip().lower() == 'true'
	elif isinstance(matchTo, int):
		return int(text)
	elif isinstance(matchTo, float):
		return float(text)
		
	else:
		raise RuntimeError('Unable to determine type of variable to parse to: {}'.format(matchTo))
