import unittest
from dirt.Node import Node
from dirt.BooleanCheck import BooleanCheck
from dirt.ChoiceCheck import ChoiceCheck
from dirt.ComparisonCheck import ComparisonCheck

class NodeTests(unittest.TestCase):
	
	def test_formatTextBlock_nonCharacter(self):
		''' covers usage of Node.formatTextBlock using the node state only '''
		node = Node('notused')
		node.addText('hell{favorite_vowel} {win_or_loss}{conjunction}{weight_abbreviation}!', lang = 'en-us')
		
		# TODO: temporary
		node.state = {'vowel': 3, 'victory': True, 'day_in_month': 9, 'weight': 2.4, 'upside_down': True}
		
		vowel = ChoiceCheck('favorite_vowel', 'node.vowel')
		vowel.addTextForValues([0], 'a')
		vowel.addTextForValues([1], 'e')
		vowel.addTextForValues([2], 'i')
		vowel.addTextForValues([3], 'o')
		vowel.addTextForValues([4], 'u')
		node.addCheck(vowel)
		
		victory = BooleanCheck('win_or_loss', 'node.victory')
		victory.addOutput(True, 'w')
		victory.addOutput(False, 'l')
		node.addCheck(victory)
		
		conjunction = ChoiceCheck('conjunction', 'node.day_in_month')
		conjunction.addTextForValues([0, 1], 'for')
		conjunction.addTextForValues([2, 3], 'and')
		conjunction.addTextForValues([4, 5], 'nor')
		conjunction.addTextForValues([6, 7], 'but')
		conjunction.addTextForValues([8, 9], 'or')
		conjunction.addTextForValues([10, 11], 'yet')
		conjunction.addTextForValues([12, 13], 'so')
		node.addCheck(conjunction)
		
		weight = ComparisonCheck('weight_abbreviation', 'node.weight')
		weight.addOutput([ComparisonCheck.Comparison(ComparisonCheck.LESS_THAN, 4.2)], 'ld', formatted = True)
		weight.addOutput([ComparisonCheck.Comparison(ComparisonCheck.EQUAL, 4.2)], 'g')
		weight.addOutput([ComparisonCheck.Comparison(ComparisonCheck.GREATER_THAN, 4.2)], 'kg')
		node.addCheck(weight)
		
		#bOrD = BooleanCheck('b_or_d', 'node.upside_down')
		#bOrD.addOutput(True, 'd')
		#bOrD.addOutput(False, 'b')
		#node.addCheck(bOrD)
		
		self.assertEqual('hello world!', node.formatTextBlock('en-us'))
		