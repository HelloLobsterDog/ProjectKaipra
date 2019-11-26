from dirt.ActionEffect import ActionEffect

class SetVarEffect(ActionEffect):
	def __init__(self, var, value):
		'''
		Intializes the effect.
		params:
		var - string containing the name of the variable to set for instance "node.xyz"
		value - string value of the variable to set.
		'''
		self.var = var
		self.value = value
	
	def trigger(self, node, viewpointCharacter, lang = 'en-us'):
		# determine name of the variable (by stripping out the dot notation) and use it to determine the dictionary that we'll be writing to
		varname = self.var
		owningDict = None
		if self.var.startswith('node.'):
			varname = self.var[5:]
			owningDict = node.state
		elif self.var.startswith('char.'):
			varname = self.var[5:]
			owningDict = viewpointCharacter.state
		else:
			raise RuntimeError('variable name prefix not recognized on variable: {}'.format(varname))
		
		# validate owning dict (and validate that it has the variable in question)
		if owningDict == None:
			raise RuntimeError('could not locate owning state dictionary')
		if not varname in owningDict:
			raise RuntimeError('variable name "{}" not found in state dictionary.'.format(varname))
		
		# convert the value to the proper type
		typeOfState = owningDict[varname].__class__
		convertedVal = self.value
		if typeOfState == int:
			convertedVal = int(self.value)
		elif typeOfState == float:
			convertedVal = float(self.value)
		elif typeOfState == bool:
			if not self.value.lower() in ['true', 'false']:
				raise ValueError('could not convert value of "{}" to bool'.format(self.value))
		else:
			raise ValueError('could not convert value of "{}" to type {}'.format(self.value, typeOfState))
		
		# finally, set it
		owningDict[varname] = convertedVal