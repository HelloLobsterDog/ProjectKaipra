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
	