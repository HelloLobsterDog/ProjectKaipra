from dirt.TemplateAction import TemplateAction

class GoTemplateAction(TemplateAction):
	
	def preempt(self, node, viewpointCharacter, lang):
		'''
		Allows the template action to preempt an action trigger, which would otherwise trigger because our text matches,
		but which cannot occur because the template action decides it can't. This is used in cases where, as an example,
		you attempt to look at something, but your character is blind - it's a valid thing to do, but the action's effects
		can't be allowed to complete by the template action stopping it.
		
		Returns a string of text to show to the user if preempting, or None if not preempting.
		'''
		return None # we don't preempt with go right now.
