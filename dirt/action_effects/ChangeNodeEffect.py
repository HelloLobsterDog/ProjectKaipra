from dirt.ActionEffect import ActionEffect

class ChangeNodeEffect(ActionEffect):
	def __init__(self, nodeID):
		self.nodeID = nodeID
	
	def trigger(self, node, viewpointCharacter, lang = 'en-us'):
		viewpointCharacter.setNode(self.nodeID)
