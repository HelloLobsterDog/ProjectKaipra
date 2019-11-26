
class ActionEffect(object):
	def trigger(self, node, viewpointCharacter, lang = 'en-us'):
		raise NotImplementedError('subclasses must override this method and implement it.')
	